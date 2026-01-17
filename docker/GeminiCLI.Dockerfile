FROM python:3.11-slim
WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git bash \
  && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x from NodeSource (reliable modern Node)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get update && apt-get install -y --no-install-recommends nodejs \
  && rm -rf /var/lib/apt/lists/*

# Install Gemini CLI
RUN npm install -g @google/gemini-cli

# Python tooling + Requests runtime deps
RUN pip install --no-cache-dir pytest requests

# Requests dev/test deps (fixtures like httpbin)
COPY requests/requirements-dev.txt /tmp/requirements-dev.txt
RUN sed '/^-e \./d' /tmp/requirements-dev.txt > /tmp/requirements-dev.filtered.txt \
  && pip install --no-cache-dir -r /tmp/requirements-dev.filtered.txt

CMD ["bash"]




# To build this Docker image, run:
# docker build -t evaluatingllm-cli-2 -f docker/GeminiCLI.Dockerfile .
