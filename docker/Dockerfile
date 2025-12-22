FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
  && rm -rf /var/lib/apt/lists/*

# Evaluation tooling.
# Install requests from PyPI here only to pull its runtime dependencies.
# At runtime we force Python to import the local reuqests repo clone via PYTHONPATH=/app/requests/src.
# TODO: update after security analysis script 
RUN pip install --no-cache-dir pytest coverage bandit ruff requests

CMD ["bash"]