#!/usr/bin/env python3

"""
Evaluate syntactic, execution and assertion correctness of generated test files.

Outputs one CSV row per collected test case (including parametrized tests).

- Checks syntax (compile) of a single test file.
- Counts 'assert' statements using the AST.
- Runs pytest on the single file and writes JUnit XML to a temporary file.
- Parses JUnit XML per-testcase to classify passes, assertion failures, and execution/import/runtime errors.
- Returns one row per collected test case with all correctness metrics.
- Cleans up temporary files.
"""


import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import py_compile
import ast
import tempfile
import csv
import argparse


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TESTS_BASE = PROJECT_ROOT / "eval" / "tests" / "generated_tests"
CSV_BASE = PROJECT_ROOT / "eval" / "results" / "correctness"


def syntactic_ok(path: Path) -> bool:
    """
    Check whether the Python file at `path` is syntactically valid.

    Attempts to compile the file with py_compile (no execution).
    Returns True when compilation succeeds, False on any compile-time error (SyntaxError, etc.) or I/O error.
    """
    try:
        # py_compile.compile raises on syntax errors when doraise=True
        py_compile.compile(str(path), doraise=True)
        return True
    except Exception:
        return False



def count_asserts(path: Path) -> int:
    """
    Count 'assert' statements in the Python source at `path`.

    Reads the file using UTF-8, parses the source to an AST and counts ast.Assert nodes.
    Returns 0 on I/O or parse errors.
    """
    try:
        
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        
        return sum(1 for n in ast.walk(tree) if isinstance(n, ast.Assert))
    except Exception:
        return 0
    

def detect_suspicious_asserts(path: Path) -> dict[str, int]:
    """
    Detect tautological assertions in the Python source at `path`.

    Filters for tautologies - assertions that are always true regardless of code behavior:
      1. Constant assertions: assert True, assert 1, assert "string", etc.
      2. Self-comparisons: assert x == x, assert foo.bar == foo.bar, etc.

    Returns a dict with counts:
      - 'constant_asserts': number of assertions with constant truthy values
      - 'self_comparison_asserts': number of assertions comparing identical expressions

    Returns {"constant_asserts": 0, "self_comparison_asserts": 0} on parse errors.
    """
    result = {"constant_asserts": 0, "self_comparison_asserts": 0}
    
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
    except Exception:
        return result

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            # Check for assert True / assert 1 / assert "string"
            if isinstance(node.test, ast.Constant):
                # node.test.value is the value of the constant
                if node.test.value:  # assert True, assert 1, etc.
                    result["constant_asserts"] += 1
            
            # Check for assert x == x
            elif isinstance(node.test, ast.Compare):
                left = node.test.left
                # Check the first comparator for simplicity
                if len(node.test.comparators) > 0:
                    right = node.test.comparators[0]
                    
                    # Compare if left and right are structurally identical
                    if ast.dump(left) == ast.dump(right):
                        result["self_comparison_asserts"] += 1

    return result
    


def run_pytest_junit(path: Path, timeout: int = 30) -> tuple[Path, str]:
    """
    Run pytest on a single test file and produce a JUnit XML file for execution correctness analysis.
    JUnit XML is used because it provides a structured and standardized way to capture passes, failures, and errors.

    Creates a temporary file (NamedTemporaryFile(delete=False)) for pytest's --junitxml output, to avoid cluttering the repo.
    Runs pytest with cwd set to the test file's parent directory, captures stdout/stderr, and enforces a timeout.

    Returns
    -------
    tuple[pathlib.Path, str]
        (xml_path, stdout_text). 
        xml_path points to the temp file that pytest should write;
        stdout_text contains pytest's terminal output and used as fallback if the XML has no useful structured messages. 
    """

    
    tmp = tempfile.NamedTemporaryFile(prefix="junit_", suffix=".xml", delete=False)
    xml_out = Path(tmp.name)
    tmp.close()  # close so pytest/other process can open/write it

    cmd = [
        "pytest",
        "-q",
        f"--junitxml={xml_out}",
        str(path),
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            cwd=str(path.parent),
        )
        out = proc.stdout or ""

    except FileNotFoundError:
        out = "pytest not found"

    except subprocess.TimeoutExpired as e:
        out = getattr(e, "stdout", None) or f"pytest timed out after {timeout}s"

    # Return the path to the XML (may or may not have been written) and captured output
    return xml_out, out


def parse_junit_cases(xml_path: Path) -> list[dict]:
    """
    Parse pytest-produced JUnit XML and return a list of testcase-level results.

    Decision criteria for execution correctness:

      - <failure> sometimes contains assertion failures or unexpected exceptions. We inspect the message: 
        1. If it looks like an AssertionError or contains an 'assert' line we treat it as a test failure 
        2. Otherwise we classify it as an execution error. 
        We do this check manually because it was observed that pytest sometimes recognizes errors as failures. 
        For example, we specifically raised a "RuntimeError" in a test and pytest reported it as a <failure>.
        We only want assertion failures to count as test failures, and everything else as execution errors.

      - <error> elements are treated as execution errors.

    Each element represents a collected test (including parametrized cases) with:
      - testcase: str (pytest-reported name, e.g. test_foo[param1])
      - status: str in {pass, failure, error, skip}
      - message: str (normalized first message text)
    """
    cases: list[dict] = []

    if not xml_path.exists():
        return cases

    try:
        root = ET.parse(xml_path).getroot()
    except Exception:
        return cases

    for testcase in root.iter("testcase"):
        name = testcase.get("name") or ""
        classname = testcase.get("classname") or ""
        failure_elem = testcase.find("failure")
        error_elem = testcase.find("error")
        skipped_elem = testcase.find("skipped")

        status = "pass"
        message = ""

        if failure_elem is not None:
            msg = failure_elem.get("message") or (failure_elem.text or "")
            msg_norm = (msg or "").strip()
            # Classify assertion vs execution error based on message content
            is_assertion = False
            if "AssertionError" in msg_norm:
                is_assertion = True
            else:
                first_line = msg_norm.splitlines()[0] if msg_norm else ""
                if first_line.startswith("assert ") or "assert " in first_line:
                    is_assertion = True

            status = "failure" if is_assertion else "error"
            message = msg_norm

        elif error_elem is not None:
            status = "error"
            message = ((error_elem.get("message") or error_elem.text or "") or "").strip()

        elif skipped_elem is not None:
            status = "skip"
            message = ((skipped_elem.get("message") or skipped_elem.text or "") or "").strip()

        cases.append({
            "testcase": name or classname,
            "status": status,
            "message": message,
        })

        
    return cases


def evaluate_cases(path: Path) -> list[dict]:
    """
    Run pytest on a single test file and return per-testcase rows.

        Steps:
      - Check syntax using syntactic_ok()
      - If syntax fails -> skip execution and assertion correctness 

      - Otherwise:
        - Count asserts using count_asserts()
        - Run pytest on the single file and produce JUnit XML (run_pytest_junit)
        - Parse JUnit XML (parse_junit)
        - Remove temporary XML file (cleanup)
        - Decide execution_ok (no execution errors) and assertion_ok (asserts present, no failures/errors, and no tautologies)
    """
    def _sanitize(msg: str, max_len: int = 500) -> str:
        """Sanitize message for CSV: flatten newlines and truncate."""
        if not msg:
            return ""
        # replace newlines and excessive whitespace with single space
        single = " ".join(msg.split())
        if len(single) > max_len:
            return single[: max_len - 3] + "..."
        return single

    if not syntactic_ok(path):
        # Return a single row with all metrics zeroed out for syntax errors
        return [{
            "file": str(path),
            "testcase": "",
            "syntactic_ok": 0,
            "execution_ok": 0,
            "assertion_ok": 0,
            "num_asserts": 0,
            "passes": 0,
            "failures": 0,
            "errors": 0,
            "skips": 0,
            "error_message": "Syntax error",
        }]

    xml, _stdout = run_pytest_junit(path)
    try:
        cases = parse_junit_cases(xml)
    finally:
        try:
            xml.unlink(missing_ok=True)
        except Exception:
            pass

    # Augment each case with per-case metrics aligned with legacy headers
    n_asserts = count_asserts(path)
    suspicious = detect_suspicious_asserts(path)
    synt_ok = int(syntactic_ok(path))

    rows: list[dict] = []
    for c in cases:
        status = c.get("status", "").lower()
        message = c.get("message", "") or ""

        passes = 1 if status == "pass" else 0
        failures = 1 if status == "failure" else 0
        errors = 1 if status == "error" else 0
        skips = 1 if status == "skip" else 0

        # Hierarchical checks: syntactic → execution → assertion
        # execution_ok: 0 if testcase has execution error, 1 otherwise
        exec_ok = 0 if status == "error" else 1
        
        # assertion_ok: only checked if execution_ok = 1
        # Requires: passing test AND file has at least one assert AND no tautological assertions
        has_tautology = (suspicious["constant_asserts"] > 0 or suspicious["self_comparison_asserts"] > 0)
        if status == "error":
            asrt_ok = 0
        elif status == "pass" and n_asserts > 0 and not has_tautology:
            asrt_ok = 1
        else:
            asrt_ok = 0

        rows.append({
            "file": str(path),
            "testcase": c.get("testcase", ""),
            "syntactic_ok": synt_ok,
            "execution_ok": exec_ok,
            "assertion_ok": asrt_ok,
            "num_asserts": n_asserts,
            "passes": passes,
            "failures": failures,
            "errors": errors,
            "skips": skips,
            "error_message": _sanitize(message) if (failures == 1 or errors == 1) else "",
        })

    return rows


def find_test_files(target: Path) -> list[Path]:
    """
    Find test files under `target`.

    If target is a file, returns [target]. Otherwise searches recursively for common
    pytest filename patterns (test_*.py and *_test.py).

    Parameters
    ----------
    target : pathlib.Path
        File or directory to search.

    Returns
    -------
    list[pathlib.Path]
        Sorted list of discovered test files.
    """
    if target.is_file():
        return [target]
    # rglob both patterns and sort the combined list for deterministic order
    return sorted(
        list(target.rglob("test_*.py")) + list(target.rglob("*_test.py"))
    )


def main():
    """
    Parses arguments, discovers test files, runs per-testcase evaluation and prints
    a human-readable summary. 
    
    Optionally writes results to a CSV file with one row per collected test case.
    Supports parametrized tests by expanding them into individual rows.

    Criteria:
        - syntactic_ok: 1 if the file compiles, 0 otherwise.
        - execution_ok: 1 if the test runs without execution errors, 0 otherwise.
        - assertion_ok: 1 if the test passes, has at least one assert, and has no tautological assertions, 0 otherwise.

    
    --strategy  : required, one of P0,P1,P2,P3 (folder under eval/tests/generated_tests)
    --tests     : optional, function name for the tests (function/class folder inside the strategy dir).
                  If omitted the whole strategy folder is evaluated.
    --csv       : optional flag. When provided the script will create CSV at:
                  eval/results/correctness/<strategy>/<tests_or_strategy>/results_<tests_or_strategy>.csv

    Examples:
      # Entire strategy
      python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --csv

      # Single subject under a strategy
      python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --tests get_auth_from_url --csv
    """

    parser = argparse.ArgumentParser(
        description="Evaluate syntactic, execution, and assertion correctness of test files."
    )
    parser.add_argument(
        "--strategy",
        required=True,
        help="Prompt generation strategy folder under eval/tests/generated_tests (e.g. P0,P1,P2,P3,R).",
    )
    parser.add_argument(
        "--tests",
        help="Function name for the tests (function/class folder inside the strategy dir). If omitted the whole strategy dir is evaluated.",
        default=None,
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="If set, create CSV at eval/results/correctness/<strategy>/<tests_or_strategy>/results_<tests_or_strategy>.csv",
    )

    args = parser.parse_args()

    strategy = args.strategy
    tests = args.tests  # may be None

    # Build target path automatically (handle tests==None)
    if tests:
        target = (TESTS_BASE / strategy / tests).resolve()
        csv_name = f"correctness_results_{tests}.csv"
    else:
        target = (TESTS_BASE / strategy).resolve()
        csv_name = f"correctness_results_{strategy}.csv"

    csv_subdir = CSV_BASE / strategy

    if not target.exists():
        print(f"No test files found at constructed path: {target}")
        return

    files = find_test_files(target)
    if not files:
        print(f"No test files found under {target}")
        return

    # Prepare CSV writer
    csv_writer = None
    csv_file = None
    fieldnames = [
        "file",
        "testcase",
        "syntactic_ok",
        "execution_ok",
        "assertion_ok",
        "num_asserts",
        "passes",
        "failures",
        "errors",
        "skips",
        "error_message",
    ]

    if args.csv:
        csv_subdir.mkdir(parents=True, exist_ok=True)
        csv_path = csv_subdir / csv_name
        csv_file = open(csv_path, "w", newline="", encoding="utf-8")
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    # Print table header
    print(f"{'file':40}  {'testcase':40}  syn  exec  asrt  asserts  pass  fail  err  skip")

    for f in files:
        rows = evaluate_cases(f)
        for r in rows:
            print(
                f"{Path(r['file']).name:40}  {r['testcase'][:40]:40}  "
                f"{int(r['syntactic_ok']):3d}  {int(r['execution_ok']):4d}  {int(r['assertion_ok']):4d}  "
                f"{int(r['num_asserts']):7d}  {int(r['passes']):4d}  {int(r['failures']):4d}  {int(r['errors']):4d}  {int(r['skips']):4d}"
            )
            if csv_writer is not None:
                csv_writer.writerow({k: r.get(k, "") for k in fieldnames})

    if csv_file is not None:
        csv_file.close()
        print(f"\nCSV written to: {csv_path}")


if __name__ == "__main__":
    main()
