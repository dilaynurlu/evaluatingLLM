FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
  && rm -rf /var/lib/apt/lists/*

# Evaluation tooling + Requests runtime deps
RUN pip install --no-cache-dir pytest coverage bandit ruff requests

# Requests dev/test deps for fixtures like "httpbin".
# Filter out "-e .[socks]" (editable install) because we don't need it in the image.
COPY requests/requirements-dev.txt /tmp/requirements-dev.txt
RUN sed '/^-e \./d' /tmp/requirements-dev.txt > /tmp/requirements-dev.filtered.txt \
  && pip install --no-cache-dir -r /tmp/requirements-dev.filtered.txt

CMD ["bash"]
