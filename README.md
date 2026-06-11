# HyperAgents-ADK Self-Learning Factor Lab

HyperAgents-ADK packages our financial self-learning agent work as a standalone Google ADK/Gemini application for the Google for Startups AI Agents Challenge, Track 1: Build (Net-new agents).

The project is a financial research assistant, not a trading bot. It helps reviewers inspect curated evidence from self-learning factor-discovery experiments, run small synthetic smoke checks, and understand validation versus held-out fragility without making investment recommendations.

## Current Status

This repository is being built incrementally. The initial skeleton includes:

- ADK package structure for `hyper_adk`, `hyper_engine_adk`, and `hyper_adk_mcp`.
- Environment/configuration scaffolding.
- A root ADK research agent with safe study-inspection tools.
- A curated first-pass study manifest.
- Curated sanitized self-learning patch examples that show how the meta process changed task-agent behavior.
- Synthetic smoke datasets for S&P 500-style and CSI300-style panels.
- A safe smoke engine with whitelisted factor templates and local run manifests.
- A read-only MCP server and MCP-client ADK agent for evidence/artifact inspection.
- Reviewer, ADK Web, and deployment guides for local testing and demo setup.
- ADK eval fixtures for research quality, smoke execution, MCP read-only behavior, and finance safety.
- Architecture and demo-script documentation with Mermaid sources.
- Docker and Cloud Run deployment scaffolding for an ADK Web public testing link.
- Submission, Devpost, and presentation strategy docs.
- Import, manifest, smoke-data, evaluator, and smoke-run tests.

Current validated baseline: `31 passed` in the dedicated `hyperagents-adk` environment, with all three ADK Web agents working on Cloud Run.

## Key Docs

| Document | Purpose |
| --- | --- |
| `IMPLEMENTATION_PLAN.md` | Running build plan and milestone log |
| `REVIEWER_INSTRUCTIONS.md` | Exact commands and pass criteria for local reviewers |
| `ADK_WEB_DEMO.md` | Browser demo guide and prompt cards |
| `DEPLOYMENT.md` | Local, MCP, Cloud Run, and optional Docker/VM deployment notes |
| `ARCHITECTURE.md` | System architecture, native ADK flow, MCP flow, and safety boundaries |
| `DEMO_SCRIPT.md` | 3-5 minute competition video walkthrough |
| `SUBMISSION.md` | Competition submission brief |
| `DEVPOST_SUBMISSION_DRAFT.md` | Copy-ready Devpost field draft |
| `PRESENTATION_STRATEGY.md` | Positioning, judging criteria map, and visual checklist |

## Public Demo

Cloud Run ADK Web testing link:

```text
https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/
```

Public demo constraints:

```text
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
```

## Smoke Test Path

The public-safe smoke path uses bundled synthetic OHLCV panels and whitelisted factor templates only. It does not launch Docker and does not execute arbitrary model-generated Python.

List bundled smoke datasets:

```bash
python -m hyper_engine.runner --list-datasets
```

Run a deterministic smoke self-learning cycle:

```bash
python -m hyper_engine.runner --dataset sp500_smoke --split val --run-id local_smoke
```

The run writes a manifest under:

```text
artifacts/runs/<run_id>/manifest.json
```

The ADK tools `list_smoke_datasets`, `run_smoke_self_learning_cycle`, `list_smoke_engine_runs`, and `inspect_smoke_engine_run` expose the same path to the agents.

## MCP Inspection

The MCP server exposes read-only inspection tools only. It intentionally excludes smoke-run execution, Docker launch, shell access, file editing, and arbitrary generated-code execution.

List MCP tools locally:

```bash
python -m hyper_adk.mcp_server --list-tools
```

The MCP-client ADK agent is available as:

```bash
adk run hyper_adk_mcp
```

## Self-Learning Evidence

The root agent can inspect sanitized examples of real self-learning patches without exposing full generated outputs, cache files, or binary diffs.

Useful ADK prompts:

```text
Explain the task-agent and meta-agent roles in this ADK version.
```

```text
List the curated self-learning patch examples and explain what changed.
```

```text
Inspect the S&P 500 task-agent patch example and summarize the safety caveats.
```

## Safety Posture

Public demo defaults keep live self-improvement and arbitrary generated-code execution disabled:

```text
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
```

Bundled sample data is for smoke testing only. It verifies installation, data loading, artifact routing, and ADK tool behavior; it does not validate financial performance.

## Setup

Use the dedicated `hyperagents-adk` conda environment for this standalone ADK submission. The original `hyperagents` environment is useful for the research repo, but reviewer setup should not depend on it.

```bash
conda env create -f environment.yml
conda activate hyperagents-adk
cp .env.example .env
pip install -e ".[eval]"
```

## Validate

```bash
python -m pytest -q
```

## Local ADK Run

After configuring Google/Gemini credentials:

```bash
adk run hyper_adk
```

or:

```bash
bash scripts/launch_adk_web_demo.sh
```
