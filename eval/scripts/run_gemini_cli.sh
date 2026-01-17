#!/usr/bin/env bash
set -euo pipefail

IMAGE="evaluatingllm-cli-2"
NETWORK_MODE="bridge"

# Guard: run from repo root
if [[ ! -d "./eval" || ! -d "./requests" ]]; then
  echo "Error: Run from evaluatingLLM project root"
  echo "Current directory: $(pwd)"
  exit 1
fi

# API key required
if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "Error: GEMINI_API_KEY is not set."
  echo "Run: export GEMINI_API_KEY='YOUR_API_KEY'"
  exit 1
fi

# Ensure target base exists (harmless)
mkdir -p eval/tests/generated_tests

echo "Starting Gemini CLI in Docker"
echo "Mounting repo RW: $(pwd) -> /workspace"
echo "Image: ${IMAGE}"
echo "Network: ${NETWORK_MODE}"
echo "Local Requests source forced via PYTHONPATH=/workspace/requests/src"
echo "Host venv hidden inside container at /workspace/venv"

docker run --rm -it \
  --network "${NETWORK_MODE}" \
  -e GEMINI_API_KEY="${GEMINI_API_KEY}" \
  -e GOOGLE_API_KEY="${GEMINI_API_KEY}" \
  -v "$(pwd)":/workspace:rw \
  -v gemini_hide_venv:/workspace/venv \
  -w /workspace \
  "${IMAGE}" \
  bash -lc 'export PYTHONPATH=/workspace/requests/src:$PYTHONPATH && exec gemini --model gemini-3-pro-preview'

