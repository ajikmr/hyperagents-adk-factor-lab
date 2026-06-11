#!/usr/bin/env bash
set -euo pipefail

cd /app

PORT="${PORT:-8080}"
HYPER_ADK_ARTIFACT_ROOT="${HYPER_ADK_ARTIFACT_ROOT:-/tmp/hyperagents-adk-artifacts}"
HYPER_ADK_DEFAULT_DATASET="${HYPER_ADK_DEFAULT_DATASET:-sp500_smoke}"

export HYPER_ADK_ARTIFACT_ROOT
export HYPER_ADK_DEFAULT_DATASET
export HYPER_ADK_ENABLE_LIVE_RUNS="${HYPER_ADK_ENABLE_LIVE_RUNS:-false}"
export HYPER_ADK_ENABLE_GENERATED_CODE="${HYPER_ADK_ENABLE_GENERATED_CODE:-false}"

mkdir -p "${HYPER_ADK_ARTIFACT_ROOT}" /tmp/hyperagents-adk-adk-artifacts

echo "Preparing HyperAgents-ADK smoke manifest for Cloud Run demo..."
python -m hyper_engine.runner \
  --dataset "${HYPER_ADK_DEFAULT_DATASET}" \
  --split val \
  --run-id cloud_run_startup_smoke || true

echo "Starting ADK Web on 0.0.0.0:${PORT}"
exec adk web . \
  --host 0.0.0.0 \
  --port "${PORT}" \
  --no-reload \
  --session_service_uri "sqlite:////tmp/hyperagents_adk_sessions.db" \
  --artifact_service_uri "file:///tmp/hyperagents-adk-adk-artifacts" \
  --log_level info
