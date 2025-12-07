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
import subprocess
import tempfile
from pathlib import Path


def run_coverage(test_root: Path, sut_root: Path, data_file: Path, timeout: int = 120) -> tuple[int, str]:
    """
    Run coverage+pytest for tests under `test_root`, storing coverage data at `data_file`.

    Executes:
        coverage run --branch --data-file=<data_file> --source=<sut_root> -m pytest <test_root>

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

    Returns
    -------
    tuple[int, str]
        - returncode: subprocess exit code
        - error_message: non-empty when an extraordinary error occurred (missing binary, timeout).
    """

    cmd = [
        "coverage", "run",
        "--branch",
        f"--data-file={data_file}",
        f"--source={sut_root}",
        "-m", "pytest",
        str(test_root),
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            cwd=str(test_root),  # run inside the test directory for stable discovery/imports
        )
        
        return proc.returncode, ""
    except FileNotFoundError:
        return -1, "coverage or pytest not found on PATH"
    except subprocess.TimeoutExpired as e:
        return -2, f"coverage run timed out after {timeout}s"


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


def main():
    """

    Behavior summary:
    - Creates temporary coverage data/json files.
    - When --json-dir is specified, keeps the JSON and .coverage artifacts for debugging.
    - Append a single row to the CSV with metrics and a short error summary (if any).
    - One row in the CSV has aggragated coverage metrics of the whole test_root (directory).
    - The same CSV can be appended to multiple times for different test roots/labels (so for different prompt strategies) but we can also create individual CSVs.
    

    Notes:
    - Requires test_root to be a directory. run_coverage is designed to run with
      cwd=test_root; passing a file would make cwd invalid. If you need per-file support, adjust cwd=test_root.parent
    - CSV is opened in append mode; header is written only when creating the file.
    - The function handles missing coverage/pytest binaries, timeouts, and other failures by
      recording a short error message in the CSV and continuing.

      Execute from the root like: python experiments/evaluate_coverage.py experiments/generated_tests/P0 --csv experiments/coverage/coverage_results.csv --json-dir coverage_debug/P0
    """
    parser = argparse.ArgumentParser(
        description="Compute line+branch coverage for a group of tests."
    )
    parser.add_argument(
        "test_root",
        help="Path to tests (directory), e.g. experiments/generated_tests/P0 (must be a directory)",
    )
    parser.add_argument(
        "--sut-root",
        default="requests/src/requests",
        help="Path to the SUT root (the code under test). Default: requests/src/requests. Change relatively if script is not run from project root",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Label for this run (e.g. P0, P1_get). Default: derived from test_root name.",
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to CSV file where results will be appended/created. Name of the file is expected",
    )
    parser.add_argument(
        "--json-dir",
        default=None,
        help="Optional directory to store coverage JSON and .coverage data for this run. "
             "Files will be named coverage_<label>.json and .coverage_<label>.",
    )
    args = parser.parse_args()

    
    test_root = Path(args.test_root).resolve()
    if not test_root.exists():
        print(f"ERROR: test_root does not exist: {test_root}")
        return
    if not test_root.is_dir():
        # run_coverage expects a directory (it sets cwd=test_root). If you need single-file runs,
        # modify cwd to path.parent and pass the file path instead.
        print(f"ERROR: test_root must be a directory: {test_root}")
        return

    sut_root = Path(args.sut_root).resolve()
    label = args.label or test_root.name
    csv_path = Path(args.csv).resolve()

    # Either keep JSON + .coverage for debugging or use temporary files
    if args.json_dir is not None:
        debug_dir = Path(args.json_dir).resolve()
        debug_dir.mkdir(parents=True, exist_ok=True)
        json_file = debug_dir / f"coverage_{label}.json"
        data_file = debug_dir / f".coverage_{label}"
        keep_debug_files = True
    else:
        # Use a TemporaryDirectory context to ensure automatic cleanup on exit
        tmp_ctx = tempfile.TemporaryDirectory()
        tmpdir = Path(tmp_ctx.name)
        json_file = tmpdir / "coverage.json"
        data_file = tmpdir / ".coverage_data"
        keep_debug_files = False

    
    print(f"Running coverage for group: {label} (tests: {test_root})")
    returncode, run_err = run_coverage(test_root, sut_root=sut_root, data_file=data_file)

    
    print("Exporting coverage JSON...")
    export_ok, export_out = export_coverage_json(data_file, json_file)

    # If export failed, produce zeroed metrics and record error text for CSV
    if not export_ok:
        print("coverage json failed:", export_out)
        metrics = {
            "total_statements": 0,
            "covered_lines": 0,
            "percent_line_coverage": 0.0,
            "total_branches": 0,
            "covered_branches": 0,
            "percent_branch_coverage": 0.0,
            "percent_total_coverage" : 0.0,
        }
        error_summary = export_out or run_err or ("coverage run returned code " + str(returncode))
    else:
        
        print("Aggregating metrics...")
        metrics = aggregate_metrics(json_file)
        
        error_summary = ""
        if returncode < 0:
            # negative codes indicate special failures reported by run_coverage (missing binary, timeout)
            error_summary = run_err
        elif returncode != 0:
            # nonzero return code (pytest failures) is not necessarily fatal for coverage generation,
            # but record it so the CSV includes that context.
            error_summary = run_err or f"coverage run returned code {returncode}"

    # Append or create CSV and include an 'error' column with a short summary
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        fieldnames = [
            "label",
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
        # keep the error cell short and single-line
        row["error"] = " ".join((error_summary or "").split())[:500]
        writer.writerow(row)

    # Report artifact locations / cleanup
    if keep_debug_files:
        print(f"Coverage JSON kept at: {json_file}")
        print(f".coverage data kept at: {data_file}")
    else:
        # ensure temporary dir is cleaned up
        tmp_ctx.cleanup()

    print(f"Done. Results appended to {csv_path}")
    print("Metrics:", metrics)


if __name__ == "__main__":
    main()
