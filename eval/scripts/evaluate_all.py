#!/usr/bin/env python3
"""
Traverse eval/tests/generated_tests and run evaluate_strategy_coverage.py and evaluate_strategy_correctness.py
for each strategy folder found.

Usage:
  python eval/scripts/evaluate_all.py [--csv] [--coverage-json] [--only-coverage] [--only-correctness]

Options:
  --csv             : pass --csv to both evaluate scripts (write CSV rows).
  --coverage-json   : pass --json-dir to evaluate_strategy_coverage (keep JSON/.coverage artifacts).
  --only-coverage   : run only coverage evaluation.
  --only-correctness: run only correctness evaluation.
  --timeout N       : per-call timeout in seconds (default 3600).
"""
import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "eval" / "scripts"
TESTS_BASE = PROJECT_ROOT / "eval" / "tests" / "generated_tests"

EVAL_COVERAGE = SCRIPTS_DIR / "evaluate_strategy_coverage.py"
EVAL_CORRECTNESS = SCRIPTS_DIR / "evaluate_strategy_correctness.py"


def run_cmd(cmd, timeout):
    print()
    print("Running:", " ".join(map(str, cmd)))
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        print(proc.stdout or "")
        return proc.returncode
    except subprocess.TimeoutExpired:
        print(f"ERROR: command timed out after {timeout}s")
        return -2
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true", help="Write CSV results (pass --csv to child scripts)")
    parser.add_argument("--coverage-json", action="store_true", help="Pass --json-dir to evaluate_strategy_coverage")
    parser.add_argument("--only-coverage", action="store_true")
    parser.add_argument("--only-correctness", action="store_true")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout per child script (seconds)")
    args = parser.parse_args()

    if not TESTS_BASE.exists():
        print(f"No generated_tests directory: {TESTS_BASE}")
        return 1

    strategies = [p.name for p in sorted(TESTS_BASE.iterdir()) if p.is_dir()]
    if not strategies:
        print(f"No strategy folders found under: {TESTS_BASE}")
        return 1

    print(f"Found strategies: {', '.join(strategies)}")
    for strat in strategies:
        print("\n" + "=" * 60)
        print(f"Processing strategy: {strat}")
        print("=" * 60)

        # coverage
        if not args.only_correctness:
            if not EVAL_COVERAGE.exists():
                print(f"evaluate_strategy_coverage.py not found at {EVAL_COVERAGE}")
            else:
                cmd = [sys.executable, str(EVAL_COVERAGE), "--strategy", strat]
                if args.csv:
                    cmd.append("--csv")
                if args.coverage_json:
                    cmd.append("--json-dir")
                rc = run_cmd(cmd, timeout=args.timeout)
                print(f"evaluate_strategy_coverage.py returned: {rc}")

        # correctness
        if not args.only_coverage:
            if not EVAL_CORRECTNESS.exists():
                print(f"evaluate_strategy_correctness.py not found at {EVAL_CORRECTNESS}")
            else:
                cmd = [sys.executable, str(EVAL_CORRECTNESS), "--strategy", strat]
                if args.csv:
                    cmd.append("--csv")
                rc = run_cmd(cmd, timeout=args.timeout)
                print(f"evaluate_strategy_correctness.py returned: {rc}")

    print("\nAll done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())