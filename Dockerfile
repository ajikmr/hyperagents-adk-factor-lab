FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    GOOGLE_GENAI_USE_VERTEXAI=true \
    GOOGLE_CLOUD_LOCATION=global \
    HYPER_ADK_MODEL=gemini-3.5-flash \
    HYPER_ADK_ENABLE_LIVE_RUNS=false \
    HYPER_ADK_ENABLE_GENERATED_CODE=false \
    HYPER_ADK_ARTIFACT_ROOT=/tmp/hyperagents-adk-artifacts \
    HYPER_ADK_DEFAULT_DATASET=sp500_smoke

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY hyper_adk ./hyper_adk
COPY hyper_adk_mcp ./hyper_adk_mcp
COPY hyper_engine ./hyper_engine
COPY hyper_engine_adk ./hyper_engine_adk
COPY sample_data ./sample_data
COPY eval ./eval
COPY assets ./assets
COPY scripts ./scripts

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

RUN chmod +x scripts/start_adk_web_cloud_run.sh scripts/launch_adk_web_demo.sh

CMD ["bash", "scripts/start_adk_web_cloud_run.sh"]
