#!/usr/bin/env python3

"""
Evaluate syntactic, execution and assertion correctness of generated test files.

- Checks syntax (compile) of a single test file.
- Counts 'assert' statements using the AST.
- Runs pytest on the single file and writes JUnit XML to a temporary file.
- Parses JUnit XML to classify passes, assertion failures, and execution/import/runtime errors.
- Returns a structured result dict and can write as row to CSV.
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


#script evaluates syntactic, execution and assertion correctness of generated tests


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


def parse_junit(xml_path: Path) -> dict:
    """
    Parse pytest-produced JUnit XML and return aggregated results and messages.

    Decision criteria for execution correctness:

      - <failure> sometimes contains assertion failures or unexpected exceptions. We inspect the message: 
        1. If it looks like an AssertionError or contains an 'assert' line we treat it as a test failure 
        2. Otherwise we classify it as an execution error. 
        We do this check manually because it was observed that pytest sometimes recognizes errors as failures. 
        For example, we specifically raised a "RuntimeError" in a test and pytest reported it as a <failure>.
        We only want assertion failures to count as test failures, and everything else as execution errors.

      - <error> elements are treated as execution errors.

      - If the XML file is missing or unparsable, a helpful message is appended to error_messages.

    Returns
    -------
    dict
        {
            "passes": int,
            "failures": int,
            "errors": int,
            "skips": int,
            "failure_messages": [str,...],
            "error_messages": [str,...]
        }
    """
    results = {
        "passes": 0,
        "failures": 0,
        "errors": 0,
        "skips": 0,
        "failure_messages": [],
        "error_messages": []
    }

    
    if not xml_path.exists():
        results["error_messages"].append(f"JUnit XML not found: {xml_path}")
        return results

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        # Parsing error
        results["error_messages"].append(f"Failed to parse JUnit XML: {e}")
        return results

    # Iterate all testcase elements and classify their outcome
    for testcase in root.iter("testcase"):
        failure_elem = testcase.find("failure")
        error_elem = testcase.find("error")
        skipped_elem = testcase.find("skipped")

        if failure_elem is not None:
            # Extract message or text for classification
            msg = failure_elem.get("message") or (failure_elem.text or "")
            msg_norm = (msg or "").strip() #Ensure msg is never None before calling strip()

            # if message mentions AssertionError or contains an 'assert' snippet -> failure. Otherwise --> error.
            is_assertion = False
            if "AssertionError" in msg_norm:
                is_assertion = True
            else:
                # Check first line for typical assert traces
                first_line = msg_norm.splitlines()[0] if msg_norm else ""
                if first_line.startswith("assert ") or "assert " in first_line:
                    is_assertion = True

            if is_assertion:
                results["failures"] += 1
                results["failure_messages"].append(msg_norm)
            else:
                results["errors"] += 1
                results["error_messages"].append(msg_norm)

        elif error_elem is not None:
            # Explicit <error> element -> execution/internal error
            msg = error_elem.get("message") or (error_elem.text or "")
            results["errors"] += 1
            results["error_messages"].append((msg or "").strip())

        elif skipped_elem is not None:
            results["skips"] += 1
        else:
            # No failure/error child -> test passed
            results["passes"] += 1

    return results


def evaluate_correctness(path: Path) -> dict:
    """
    Evaluate a single test file for syntactic, execution and assertion correctness.

    Steps:
      - Check syntax using syntactic_ok()
      - If syntax fails -> skip execution and assertion correctness 

      - Otherwise:
        - Count asserts using count_asserts()
        - Run pytest on the single file and produce JUnit XML (run_pytest_junit)
        - Parse JUnit XML (parse_junit)
        - Remove temporary XML file (cleanup)
        - Decide execution_ok (no execution errors) and assertion_ok (asserts present and no failures/errors)

    Parameters
    ----------
    path : pathlib.Path
        Path to the test file to evaluate.

    Returns
    -------
    dict
        Summary containing:
          - file: str
          - syntactic_ok: int (1/0)
          - execution_ok: int (1/0)
          - assertion_ok: int (1/0)
          - num_asserts: int
          - passes, failures, errors, skips: int
          - pytest_stdout_tail: str (last lines of pytest output for diagnostics)
    """
    
    syntax = syntactic_ok(path)
    if not syntax:
        return {
            "file": str(path),
            "syntactic_ok": int(syntax),
            "execution_ok": 0,
            "assertion_ok": 0,
            "num_asserts": 0,
            "passes": 0,
            "failures": 0,
            "errors": 0,
            "skips": 0,
            "error_message": "",
            "pytest_stdout_tail": "skipped due to syntax error",
        }

    n_asserts = count_asserts(path)

    xml, stdout = run_pytest_junit(path)
    try:
        junit = parse_junit(xml)
    finally:
        try:
            xml.unlink(missing_ok=True)
        except Exception:
            pass

    exec_ok = (junit.get("errors", 0) == 0)

    # assertion_ok only true when asserts exist and there are no failures or execution errors
    if n_asserts == 0:
        assert_ok = False
    elif junit.get("failures", 0) > 0:
        assert_ok = False
    elif junit.get("errors", 0) > 0:
        assert_ok = False
        #TODO: we could set n_asserts to 0 here to indicate that because of the execution error we skipped the assertion check
    else:
        assert_ok = True

    # Build a concise single-line error_message for CSV:
    # - Prefer structured messages from parse_junit()
    # - For assertion failures include failure_messages; for execution errors include error_messages
    # - Only include a message when failures/errors exist; otherwise leave empty
    def _sanitize(msg: str, max_len: int = 500) -> str:
        if not msg:
            return ""
        # replace newlines and excessive whitespace with single space
        single = " ".join(msg.split())
        if len(single) > max_len:
            return single[: max_len - 3] + "..."
        return single

    error_message = ""
    if junit.get("errors", 0) > 0:
        msgs = junit.get("error_messages", []) or []
        if msgs:
            error_message = _sanitize("; ".join(msgs))
        else:
            # fallback to last few lines of stdout (if any)
            error_message = _sanitize("\n".join((stdout or "").splitlines()[-10:]))
    elif junit.get("failures", 0) > 0:
        msgs = junit.get("failure_messages", []) or []
        if msgs:
            error_message = _sanitize("; ".join(msgs))
        else:
            error_message = _sanitize("\n".join((stdout or "").splitlines()[-10:]))
    else:
        # no failures/errors -> keep empty to avoid including passing stdout in CSV
        error_message = ""

    return {
        "file": str(path),
        "syntactic_ok": int(syntax),
        "execution_ok": int(exec_ok),
        "assertion_ok": int(assert_ok),
        "num_asserts": n_asserts,
        "passes": junit.get("passes", 0),
        "failures": junit.get("failures", 0),
        "errors": junit.get("errors", 0),
        "skips": junit.get("skips", 0),
        "error_message": error_message,
        "pytest_stdout_tail": "\n".join((stdout or "").splitlines()[-30:]),
    }


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

    Parses arguments, discovers test files, runs evaluate_correctness on each file and prints
    a human-readable summary. 
    
    Optionally writes results to a CSV file including all scores and the error message.
    In one line of the CSV, we have results for one test case. 
    (Each test case is saved in a separate .py file for clear observation.)

    The script can be called for a single test file or an entire folder.

    Criteria:
        - syntactic_ok: 1 if the file compiles, 0 otherwise. If 0, we skip execution and assertion checks.
        - exectution_ok: 1 if the test runs without execution errors, 0 otherwise.
        - assertion_ok: 1 if there is at least one assert and no execution failures and no assertion failures, 0 otherwise.

    Call from root directorty like so:
      python3 experiments/evaluate_correctness.py experiments/generated_tests --csv results_correctness.csv
    """
    parser = argparse.ArgumentParser(
        description="Evaluate syntactic, execution, and assertion correctness of test files."
    )
    parser.add_argument(
        "path",
        help="Test file or directory (e.g. experiments/generated_tests)"
    )
    parser.add_argument(
        "--csv",
        help="Optional path to write CSV results (e.g. results_correctness.csv). Creates or overwrites existing file.",
        default=None,
    )
    args = parser.parse_args()

    target = Path(args.path).resolve()
    files = find_test_files(target)
    if not files:
        print(f"No test files found under {target}")
        return

    # Prepare CSV writer if requested
    csv_writer = None
    csv_file = None
    fieldnames = [
        "file",
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


    if args.csv is not None:
        #w - creates a new file or overwrites existing
        csv_file = open(args.csv, "w", newline="", encoding="utf-8")
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    # Print table header
    print(f"{'file':60}  syn  exec  asrt  asserts  pass  fail  err  skip")

    for f in files:
        result = evaluate_correctness(f)

        # Print human-readable row
        print(
            f"{Path(result['file']).name:60}  "
            f"{result['syntactic_ok']:3d}  "
            f"{result['execution_ok']:4d}  "
            f"{result['assertion_ok']:4d}  "
            f"{result['num_asserts']:7d}  "
            f"{result['passes']:4d}  "
            f"{result['failures']:4d}  "
            f"{result['errors']:4d}  "
            f"{result['skips']:4d}"
        )

        # Write CSV row if requested
        if csv_writer is not None:
            csv_writer.writerow({k: result.get(k, "") for k in fieldnames})

    if csv_file is not None:
        csv_file.close()
        print(f"\nCSV written to: {args.csv}")


if __name__ == "__main__":
    main()
