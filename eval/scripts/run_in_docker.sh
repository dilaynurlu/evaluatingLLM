#!/usr/bin/env bash
set -euo pipefail

# RUN FROM PROJECT ROOT evaluatingLLM/
# 
# Run any evaluation script command inside the Docker sandbox. Give the whole evaluation command as input.
# Usage examples:
#   ./eval/scripts/run_in_docker.sh python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --csv
#   ./eval/scripts/run_in_docker.sh python eval/scripts/evaluate_strategy_coverage.py --strategy P0 --tests _basic_auth_str --csv --json-dir
#   ./eval/scripts/run_in_docker.sh python eval/scripts/evaluate_strategy_coverage.py --requests --csv
#
# Options:
#   --net        enable network (default: disabled)
#   --image NAME docker image tag (default: evaluatingllm-eval)

IMAGE="evaluatingllm-eval"
NETWORK_MODE="none"

# Parse optional flags for this wrapper
while [[ $# -gt 0 ]]; do
  case "$1" in
    --net)
      NETWORK_MODE="bridge"
      shift
      ;;
    --image)
      IMAGE="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [--net] [--image NAME] <command...>"
      exit 0
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 1 ]]; then
  echo "Error: no command provided."
  echo "Example: $0 python eval/scripts/evaluate_strategy_correctness.py --strategy P0 --csv"
  exit 1
fi

# Ensure results dir exists on host so the bind mount works
mkdir -p eval/results

# Run inside Docker FROM PROJECT ROOT:
# - repo read-only for safety
# - eval/results writable so CSVs are written 
# - mount local repo to install requests from local clone
docker run --rm \
  --network "${NETWORK_MODE}" \
  -v "$(pwd)":/app:ro \
  -v "$(pwd)/eval/results":/app/eval/results:rw \
  -v "$(pwd)/eval/tests/generated_tests":/app/eval/tests/generated_tests:rw \
  -w /app \
  "${IMAGE}" \
  bash -lc 'export PYTHONPATH=/app/requests/src:$PYTHONPATH && "$@"' -- "$@"

