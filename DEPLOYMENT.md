# HyperAgents-ADK Deployment Notes

This document describes practical deployment and testing paths for HyperAgents-ADK.

Current status:

- Local unit/smoke tests are validated.
- Safe synthetic smoke execution is implemented.
- Read-only MCP server and MCP-client agent are implemented.
- Local ADK CLI and ADK Web are the next runtime validation targets after installing ADK dependencies.
- Cloud Run ADK Web deployment scaffolding is included for the recommended public testing link path.
- Original Docker-based HyperAgents reproduction is optional/private and intentionally not part of the public demo path.

## Deployment Modes

| Mode | Status | Purpose |
| --- | --- | --- |
| Local tests | Validated | Fastest package and smoke-engine check |
| Local smoke CLI | Validated | Self-contained synthetic factor-template evaluation |
| Local ADK CLI | Supported after ADK deps/credentials | Fast reviewer prompt testing |
| ADK Web | Supported after ADK deps/credentials | Browser-based demo and tool traces |
| Local stdio MCP | Implemented | Read-only evidence/artifact inspection through MCP |
| Cloud Run ADK Web | Deployment scaffold included | Public Devpost testing link |
| Optional Docker/VM reproduction | Not public default | Advanced/private original-study reproduction only |

## Prerequisites

Use the dedicated `hyperagents-adk` conda environment. Do not require the original research `hyperagents` environment for the public ADK submission path.

```bash
cd HyperAgents/adk_related/hyperagents_adk
conda env create -f environment.yml
conda activate hyperagents-adk
cp .env.example .env
pip install -e ".[eval]"
```

Configure Google credentials for ADK/Gemini commands:

```bash
gcloud auth login
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

Recommended `.env` values:

```bash
HYPER_ADK_MODEL=gemini-3.5-flash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
HYPER_ADK_DEPLOY_REGION=asia-south1
HYPER_ADK_ARTIFACT_ROOT=./artifacts
HYPER_ADK_DEFAULT_DATASET=sp500_smoke
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
```

`GOOGLE_CLOUD_LOCATION=global` is the recommended model-serving location unless the selected Gemini model is confirmed in a regional Vertex location.

## Mode 1: Local Validation

```bash
python -m pytest -q
python -m hyper_engine.runner --list-datasets
python -m hyper_engine.runner --dataset sp500_smoke --split val --run-id local_smoke
python -m hyper_adk.mcp_server --list-tools
```

The smoke run writes:

```text
artifacts/runs/<run_id>/manifest.json
```

Safety fields should include:

```text
docker_launched: false
arbitrary_generated_code_executed: false
template_execution_only: true
```

## Mode 2: Local ADK CLI

Run the main agent:

```bash
adk run hyper_adk "Explain the task-agent and meta-agent roles in this ADK version."
```

Run the smoke-cycle agent:

```bash
adk run hyper_engine_adk "Run a smoke self-learning cycle on the bundled S&P 500 smoke data and summarize the caveats."
```

Run the MCP-client agent:

```bash
adk run hyper_adk_mcp "List available self-learning studies through MCP and explain the evidence caveats."
```

## Mode 3: Local ADK Web

Start ADK Web:

```bash
bash scripts/launch_adk_web_demo.sh
```

This wraps:

```bash
adk web . --host 127.0.0.1 --port 8501 --no-reload --log_level info
```

Open:

```text
http://127.0.0.1:8501
```

Select one of:

```text
hyper_adk
hyper_engine_adk
hyper_adk_mcp
```

Use prompt cards from `ADK_WEB_DEMO.md`.

## Mode 4: Local MCP Server

List exposed MCP tools:

```bash
python -m hyper_adk.mcp_server --list-tools
```

The MCP server exposes read-only tools such as:

```text
list_available_studies
get_study_summary
compare_conditions
list_learning_patch_examples
inspect_learning_patch
explain_task_meta_roles
list_smoke_datasets
list_smoke_engine_runs
inspect_smoke_engine_run
finance_safety_check
```

It intentionally excludes:

```text
run_smoke_self_learning_cycle
Docker launch
shell access
file editing
arbitrary generated-code execution
```

## Mode 5: Cloud Run ADK Web Testing Link

Cloud Run is the recommended path for a public Devpost testing link.

Target demo architecture:

```text
Cloud Run service: ADK Web serving hyper_adk, hyper_engine_adk, hyper_adk_mcp
Vertex AI: Gemini model serving
Bundled sample_data: synthetic smoke data
Container-local artifacts: ephemeral smoke run manifests
MCP: local stdio server for read-only tools inside the ADK container
```

Recommended public-demo constraints:

- Keep `HYPER_ADK_ENABLE_LIVE_RUNS=false`.
- Keep `HYPER_ADK_ENABLE_GENERATED_CODE=false`.
- Do not expose the original Docker daemon.
- Do not set provider keys for non-Google model backends.
- Use Vertex AI through the Cloud Run service account.
- Treat local artifacts as ephemeral demo state.
- Use GCS later only if persistent artifact storage is needed.

Cloud Run service account needs:

```text
roles/aiplatform.user
```

Deploy from the standalone repository root:

```bash
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
export HYPER_ADK_DEPLOY_REGION=asia-south1
bash scripts/deploy_cloud_run_adk_web.sh
```

The script runs:

```bash
gcloud run deploy hyperagents-adk-factor-lab --source . --allow-unauthenticated
```

and sets safe public-demo environment variables:

```text
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_LOCATION=global
HYPER_ADK_MODEL=gemini-3.5-flash
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
HYPER_ADK_ARTIFACT_ROOT=/tmp/hyperagents-adk-artifacts
HYPER_ADK_DEFAULT_DATASET=sp500_smoke
```

The container startup script creates a small startup smoke manifest under `/tmp` and then starts ADK Web on Cloud Run's `PORT`.

After deployment, use the Cloud Run service URL as the Devpost testing access link. The direct ADK UI path is usually:

```text
https://SERVICE_URL/dev-ui/
```

Current deployed public demo:

```text
https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/
```

Verified service environment:

```text
GOOGLE_CLOUD_LOCATION=global
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
HYPER_ADK_DEFAULT_DATASET=sp500_smoke
```

## Mode 6: Optional Original Docker/VM Reproduction

The original HyperAgents study used Docker to evaluate self-modifying agents and generated Python strategy code. That path is not the public default because it is slower, more brittle, and involves untrusted generated-code execution.

If a deeper reproduction mode is added later, it should be private or local and follow these rules:

- Fixed command templates only.
- No user-supplied shell commands.
- No arbitrary repo path or image name.
- Tiny synthetic smoke data only unless the operator has the original research data.
- Hard timeout and resource limits.
- Dedicated service account with minimal permissions.
- Artifacts written to local storage or GCS for read-only inspection.
- No public unauthenticated endpoint that can launch Docker jobs.

Recommended public competition posture:

```text
Cloud Run ADK Web = public interactive demo
Local smoke CLI = reviewer-verifiable execution
Read-only MCP = safe integration proof
Original Docker loop = optional/private research reproduction
```
