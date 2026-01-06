#!/usr/bin/env python3
"""
Evaluate line & branch coverage for a group of tests using coverage.py.

- Runs: coverage run --branch --source=<sut_root> -m pytest <test_root>
- Intended to be run on a whole directory of tests per strategy, so test_root is mainly a directory,
- Exports: coverage json -o <json_file>
- Aggregates metrics across all SUT files.
- Appends a single row to a CSV (one row per run/label).
- If --json-dir is provided, also keeps the JSON and .coverage files
  for later debugging / HTML reports.
"""

import argparse
import csv
import json
import re
import subprocess
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TESTS_BASE = PROJECT_ROOT / "eval" / "tests" / "generated_tests"
CSV_BASE = PROJECT_ROOT / "eval" / "results" / "coverage"
FUNCTIONS_TO_TEST_JSON = PROJECT_ROOT / "eval" / "functions" / "functions_to_test.json"

def run_coverage(
    test_root: Path,
    sut_root: Path,
    data_file: Path,
    timeout: int = 120,
    pytest_args: list[str] | None = None,
) -> tuple[int, str, dict]:
    """
    Run coverage+pytest for tests under `test_root`, storing coverage data at `data_file`.

    Executes:
       no pytest_args: coverage run --branch --data-file=<data_file> --source=<sut_root> -m pytest <test_root> 
       given pytest_args: coverage run --branch --data-file=<data_file> --source=<sut_root> -m pytest <pytest_args>

    Parameters
    ----------
    test_root : pathlib.Path
        Directory containing tests to run (assumed to be a directory and sets cwd to it).
    sut_root : pathlib.Path
        Path to the SUT root to pass as --source to coverage. 
        Specifies exactly which files will be measured for coverage (the requests src).
        Avoids that the test case itself shows up in the coverage measurement.
    data_file : pathlib.Path
        Path to the .coverage data file (passed via --data-file).
    timeout : int, optional
        Seconds to wait for coverage/pytest to finish before killing the process.
    pytest_args : list[str] | None
        This will be a list of test nodeids to pass to pytest so that only those tests are run.
        If None, all tests under test_root are run.
        


    Returns
    -------
    tuple[int, str, dict]
        - returncode: subprocess exit code
        - error_message: non-empty when an extraordinary error occurred (missing binary, timeout).
        - test_stats: dict with parsed pytest stats, e.g. {"tests_run": int, "collected": int}. How many tests for coverage
    """

    cmd = [
        "coverage", "run",
        "--branch",
        f"--data-file={data_file}",
        f"--source={sut_root}",
        "-m", "pytest", "-v",
    ]

    if pytest_args:
        cmd.extend(pytest_args) 
        #no need to append test_root 
    else: 
        cmd.append(str(test_root))
        # If no explicit pytest_args, run all tests under test_root
    

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT), 
        )

        print(proc.stdout)

        test_stats = _parse_pytest_test_counts(proc.stdout)
        return proc.returncode, "", test_stats
    except FileNotFoundError:
        return -1, "coverage or pytest not found on PATH", {"tests_run": 0, "collected": 0}
    except subprocess.TimeoutExpired as e:
        return -2, f"coverage run timed out after {timeout}s", {"tests_run": 0, "collected": 0}


def _parse_pytest_test_counts(output: str) -> dict:
    """
    Parse pytest output text to estimate how many tests actually ran.

    Returns a dict with keys:
      - tests_run: sum of executed test outcomes (passed, failed, error(s), skipped, xfailed, xpassed, rerun(s))
      - collected: number reported by "collected N items" if present, else 0

    Notes:
    - Pytest prints a summary like "=== 5 passed, 1 skipped in 0.30s ===".
      We scan the entire output for tokens of the form "<num> <keyword>" where
      keyword is one of the recognized outcome words, and sum them.
    - "warnings" and "deselected" are not counted as executed tests.
    """
    if not output:
        return {"tests_run": 0, "collected": 0}

    # Count outcomes from summary lines
    outcome_map = {
        "passed": "passed",
        "failed": "failed",
        "error": "error",
        "errors": "error",
        "skipped": "skipped",
        "xfailed": "xfailed",
        "xpassed": "xpassed",
        "rerun": "rerun",
        "reruns": "rerun",
    }

    totals: dict[str, int] = {k: 0 for k in set(outcome_map.values())}
    for num, word in re.findall(r"(\d+)\s+(passed|failed|error|errors|skipped|xfailed|xpassed|rerun|reruns)\b", output):
        totals[outcome_map[word]] += int(num)

    tests_run = sum(totals.values())

    # Parse collected items line, e.g., "collected 12 items" or "collected 12 items / 2 deselected"
    m = re.search(r"collected\s+(\d+)\s+items?\b", output)
    collected = int(m.group(1)) if m else 0

    return {"tests_run": tests_run, "collected": collected}


def export_coverage_json(data_file: Path, json_path: Path, timeout: int = 30) -> tuple[bool, str]:
    """
    Convert a coverage data file into coverage.json.

    Executes:
        coverage json --pretty-print --data-file=<data_file> -o <json_path>

    Parameters
    ----------
    data_file : pathlib.Path
        Path to the .coverage data file produced by `coverage run`.
    json_path : pathlib.Path
        Destination path for the produced JSON report.
    timeout : int
        Seconds to wait for the `coverage json` subprocess before treating it as failed.

    Returns
    -------
    tuple[bool, str]
        (success, output_text). On success success=True and output_text contains any CLI output;
        on failure success=False and output_text contains a human-readable error or captured output.

    Notes
    -----
    - This function runs the subprocess with cwd set to data_file.parent to make behavior
      deterministic when coverage expects relative paths.
    """
    
    if not data_file.exists():
        return False, f"coverage data file not found: {data_file}"

    cmd = [
        "coverage", "json", "--pretty-print",
        f"--data-file={data_file}",
        "-o", str(json_path),
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            cwd=str(data_file.parent),
        )
        out = proc.stdout or ""
        if proc.returncode != 0:
            return False, out or f"'coverage json' exited with code {proc.returncode}"
        return True, out
    except FileNotFoundError:
        return False, "coverage CLI not found on PATH"
    except subprocess.TimeoutExpired as e:
        return False, getattr(e, "stdout", "") or f"'coverage json' timed out after {timeout}s"


def aggregate_metrics(json_path: Path) -> dict:
    """
    Parse coverage JSON and aggregate line & branch metrics
    across all files in the json report (which correspond to SUT files).
    """
    
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "total_statements": 0,
            "covered_lines": 0,
            "percent_line_coverage": 0.0,
            "total_branches": 0,
            "covered_branches": 0,
            "percent_branch_coverage": 0.0,
            "percent_total_coverage" : 0.0,
        }

    files = data.get("files", {})

    total_statements = 0
    covered_lines = 0
    total_branches = 0
    covered_branches = 0

    for info in files.values():
        summary = info.get("summary", {})
        num_stmts = summary.get("num_statements", 0)
        cov_lines = summary.get("covered_lines", 0)
        num_br = summary.get("num_branches", 0)
        cov_br = summary.get("covered_branches", 0)

        total_statements += num_stmts
        covered_lines += cov_lines
        total_branches += num_br
        covered_branches += cov_br

    percent_line_cov = (covered_lines / total_statements * 100.0) if total_statements > 0 else 0.0
    percent_branch_cov = (covered_branches / total_branches * 100.0) if total_branches > 0 else 0.0

    #Formula from coverage.py documentation on https://coverage.readthedocs.io/en/7.12.0/faq.html
    denominator = total_statements + total_branches
    percent_total_cov = ((covered_lines + covered_branches) / denominator * 100.0) if denominator > 0 else 0.0

    return {
        "total_statements": total_statements,
        "covered_lines": covered_lines,
        "percent_line_coverage": percent_line_cov,
        "total_branches": total_branches,
        "covered_branches": covered_branches,
        "percent_branch_coverage": percent_branch_cov,
        "percent_total_coverage" : percent_total_cov
    }


def build_requests_functions_pytest_args(function_name: str | None) -> list[str]:
    """
    Build pytest args using exact nodeids stored in JSON under test_cases[].test_nodeid.

    Expected JSON nodeid format (project-root relative):
        "requests/tests/test_utils.py::TestUtils::test_foo"
        "requests/tests/test_utils.py::test_bar"

    Returns a list of absolute-path nodeids, safe for class-based tests.
    """
    if not FUNCTIONS_TO_TEST_JSON.exists():
        raise FileNotFoundError(f"functions_to_test.json not found at {FUNCTIONS_TO_TEST_JSON}")

    raw = json.loads(FUNCTIONS_TO_TEST_JSON.read_text(encoding="utf-8"))

    # Filter by JSON entry name if requested
    if function_name is not None:
        filtered = [entry for entry in raw if entry.get("name") == function_name]
        if not filtered:
            available = sorted({e.get("name") for e in raw if "name" in e})
            raise ValueError(
                f'No entry with name="{function_name}" in {FUNCTIONS_TO_TEST_JSON}. '
                f"Available names: {available}"
            )
        raw = filtered

    nodeids: set[str] = set()

    # Make sure that the given node ids are absolute paths for pytest. JSON file gives them relative
    for entry in raw:
        for tc in entry.get("test_cases", []):
            nid = tc.get("test_nodeid")
            if not nid:
                continue

            nid = str(nid).strip()
            if not nid or nid.startswith("#"):
                continue

            # Split "file_path::rest..." like in "requests/tests/test_utils.py::TestUtils::test_foo"
            parts = nid.split("::", 1)
            file_part = parts[0].strip()
            rest = parts[1] if len(parts) == 2 else ""

            # Turn file_part into a absolute Path
            file_path = Path(file_part)
            if not file_path.is_absolute():
                file_path = (PROJECT_ROOT / file_part).resolve() #now absolute 
            else:
                file_path = file_path.resolve()

            if not file_path.exists():
                raise FileNotFoundError(f"Test file from test_nodeid not found: {file_path} (nodeid={nid})")

            # https://docs.pytest.org/en/stable/how-to/usage.html#select-tests
            #Build back an absolute nodeid by adding the rest back 
            abs_nodeid = str(file_path) + (f"::{rest}" if rest else "")
            nodeids.add(abs_nodeid)

    if not nodeids:
        raise ValueError("No test_nodeid values found after filtering functions_to_test.json")

    return sorted(nodeids)





def main():
    """

    Behavior summary:
    - Creates temporary coverage data/json files.
    - When --json-dir is specified, keeps the JSON and .coverage artifacts for debugging.
    - Appends a single row to the CSV with metrics and a short error summary.
    - One row in the CSV has aggragated coverage metrics of the whole test_root. 
    - Recommended to run this script once per strategy folder. 
    

    Notes:
    - Requires test_root to be a directory. run_coverage is designed to run with
      cwd=test_root; passing a file would make cwd invalid. If you need per-file support, adjust cwd=test_root.parent
    - The function handles missing coverage/pytest binaries, timeouts, and other failures by
      recording a short error message in the CSV and continuing.

    CLI:
      --strategy                (required unless --requests) : e.g. P0, P1, ...
      --tests                   (optional)                  : tests folder under the strategy to run (e.g. get_auth_from_url)
      --requests-all            (flag)                      : runs all the tests under requests repo at <project_root>/requests/tests
      --reqests-functions  (flag)                      : runs only the example reuqests library test cases that were listed on the functions_to_test.json. For fair coverage comparison between generated LLM tests and official requests tests.     
      --sut-root                (optional)                  : path to SUT root, default requests/src/requests
      --label                   (optional)                  : friendly label used in CSV/JSON filenames
      --csv                     (flag)                      : write CSV to eval/results/coverage/<strategy_or_requests>/coverage_results_<label>.csv
      --json-dir                (flag)                      : keep coverage JSON/.coverage under eval/results/coverage/<strategy_or_requests>/json_results/

      Usage examples:
      python ./eval/scripts/evaluate_strategy_coverage.py --strategy P0 --tests _basic_auth_str --csv --json-dir
      python ./eval/scripts/evaluate_strategy_coverage.py --requests --csv
      python ./eval/scripts/evaluate_strategy_coverage.py --requests-functions --name get_auth_from_url --csv --json-dir
    """
    parser = argparse.ArgumentParser(
        description="Compute line+branch coverage for a group of tests."
    )
    parser.add_argument(
        "--strategy",
        help="Prompt generation strategy folder under eval/tests/generated_tests (e.g. P0,P1,P2).",
        default=None,
    )
    parser.add_argument(
        "--tests",
        help="Optional subject folder inside the strategy (or inside requests/tests when --requests).",
        default=None,
    )
    parser.add_argument(
        "--requests-all",
        action="store_true",
        help="Run the whole of requests project's own test-suite under <project_root>/requests/tests instead of generated_tests.",
    )
    parser.add_argument(
        "--requests-functions",
        action="store_true",
        help="Run only the example requests library test cases that were listed on the functions_to_test.json for fair coverage comparison between generated LLM tests and official requests tests. We should not run all tests in requests if we want fair coverage, because not all of them are relavant to the functions we generated LLM tests for.",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Only to be used when --requests-functions is set. Execute coverage for only one function (name) from functions_to_test.json. If name is not given, runs all functions listed in functions_to_test.json.",
    )
    parser.add_argument(
        "--sut-root",
        default="requests/src/requests",
        help="Path to the SUT root (the code under test). Default: requests/src/requests",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Label for this run (used in CSV and JSON filenames). Defaults to tests (if given) or strategy/requests.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="If set, create CSV at eval/results/coverage/<strategy_or_requests>/coverage_results_<label>.csv",
    )
    parser.add_argument(
        "--json-dir",
        action="store_true",
        help="If set, keep coverage JSON and .coverage files under eval/results/coverage/<strategy_or_requests>/json_results/ (auto-created).",
    )

    args = parser.parse_args()
    pytest_args = None # default. If --requests-functions is used, will be set to specific test nodeids by build_requests_functions_pytest_args()

    # Determine test_root
    if args.requests_all and args.requests_functions:
        parser.error("Choose only one: --requests-all OR --requests-functions")

    if args.requests_all:
        # ignore --strategy, run the official requests tests
        test_root = (PROJECT_ROOT / "requests" / "tests").resolve()
        strategy_for_csv = "requests-all"
        label = args.label or "requests-all"

    elif args.requests_functions:
        test_root = (PROJECT_ROOT / "requests" / "tests").resolve() #this actually wont be passed to pytest from run_coverage since we provide pytest.args

        pytest_args = build_requests_functions_pytest_args(args.name)

        if args.name:
            strategy_for_csv = f"requests-functions-{args.name}"
            label = args.label or f"requests-functions-{args.name}"
        else:
            strategy_for_csv = "requests-functions"
            label = args.label or "requests-functions"

    else:
        # --strategy is required when not using --requests
        if not args.strategy:
            parser.error("--strategy is required when neither --requests-all nor --requests-functions is set")
        strategy = args.strategy
        if args.tests:
            test_root = (TESTS_BASE / strategy / args.tests).resolve()
            label = args.label or args.tests
        else:
            test_root = (TESTS_BASE / strategy).resolve()
            label = args.label or strategy
        strategy_for_csv = strategy

    if not test_root.exists():
        print(f"ERROR: test_root does not exist: {test_root}")
        return
    if not test_root.is_dir():
        print(f"ERROR: test_root must be a directory: {test_root}")
        return

    sut_root = (PROJECT_ROOT / args.sut_root).resolve()

    # CSV path: always under eval/results/coverage/<strategy_or_requests>/coverage_results_<label>.csv
    csv_dir = CSV_BASE / strategy_for_csv
    csv_path = csv_dir / f"coverage_results_{label}.csv"

    
    if args.json_dir:
        debug_dir = csv_dir / "json_results"
        debug_dir.mkdir(parents=True, exist_ok=True)
        json_file = debug_dir / f"coverage_{label}.json"
        data_file = debug_dir / f".coverage_{label}"
        keep_debug_files = True
    else:
        tmp_ctx = tempfile.TemporaryDirectory()
        tmpdir = Path(tmp_ctx.name)
        json_file = tmpdir / "coverage.json"
        data_file = tmpdir / ".coverage_data"
        keep_debug_files = False



    print(f"\nRunning coverage for group: {label} (tests: {test_root})")
    returncode, run_err, test_stats = run_coverage(
        test_root, sut_root=sut_root, data_file=data_file, pytest_args=pytest_args,
    )

    print("\nExporting coverage JSON...")
    export_ok, export_out = export_coverage_json(data_file, json_file)

    if not export_ok:
        print("\ncoverage json failed:", export_out)
        metrics = {
            "total_statements": 0,
            "covered_lines": 0,
            "percent_line_coverage": 0.0,
            "total_branches": 0,
            "covered_branches": 0,
            "percent_branch_coverage": 0.0,
            "percent_total_coverage": 0.0,
        }
        error_summary = export_out or run_err or ("coverage run returned code " + str(returncode))
    else:
        print("\nAggregating metrics...")
        metrics = aggregate_metrics(json_file)
        error_summary = ""
        if returncode < 0:
            error_summary = run_err
        elif returncode != 0:
            error_summary = run_err or f"coverage run returned code {returncode}"

    # Append to CSV 
    if args.csv:
        csv_dir.mkdir(parents=True, exist_ok=True)
        write_header = not csv_path.exists()
        with csv_path.open("a", newline="", encoding="utf-8") as f:
            fieldnames = [
                "label",
                "tests_run",
                "total_statements",
                "covered_lines",
                "percent_line_coverage",
                "total_branches",
                "covered_branches",
                "percent_branch_coverage",
                "percent_total_coverage",
                "error",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            row = {"label": label}
            row.update(metrics)
            row["tests_run"] = int(test_stats.get("tests_run", 0))
            row["error"] = " ".join((error_summary or "").split())[:500]
            writer.writerow(row)
        print(f"\nResults appended to {csv_path}")

    if keep_debug_files:
        print(f"\nCoverage JSON kept at: {json_file}")
        print(f"\n.coverage data kept at: {data_file}")
    else:
        tmp_ctx.cleanup()

    print("\nMetrics:", metrics)


if __name__ == "__main__":
    main()
