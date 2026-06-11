#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-}"
REGION="${HYPER_ADK_DEPLOY_REGION:-asia-south1}"
SERVICE_NAME="${HYPER_ADK_CLOUD_RUN_SERVICE:-hyperagents-adk-factor-lab}"

if [[ -z "${PROJECT_ID}" ]]; then
  echo "GOOGLE_CLOUD_PROJECT must be set." >&2
  exit 1
fi

echo "Deploying ${SERVICE_NAME} to Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"

gcloud config set project "${PROJECT_ID}"

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com

gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region "${REGION}" \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 900 \
  --max-instances 2 \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=global,HYPER_ADK_MODEL=gemini-3.5-flash,HYPER_ADK_ENABLE_LIVE_RUNS=false,HYPER_ADK_ENABLE_GENERATED_CODE=false,HYPER_ADK_ARTIFACT_ROOT=/tmp/hyperagents-adk-artifacts,HYPER_ADK_DEFAULT_DATASET=sp500_smoke"

echo
echo "Deployment complete. Use the Cloud Run service URL as the Devpost testing access link."
echo "Live self-improvement and generated-code execution are disabled in Cloud Run by default."
