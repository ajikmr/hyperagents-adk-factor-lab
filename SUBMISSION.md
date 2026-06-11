# HyperAgents-ADK Submission Brief

## Project Summary

HyperAgents-ADK Self-Learning Factor Lab is a Google ADK and Gemini-powered financial research agent for safe self-learning factor discovery.

The project adapts our HyperAgents financial self-learning research into a standalone Track 1 agent application. It preserves the core task-agent/meta-agent architecture while making the reviewer-facing demo bounded, auditable, and safe: synthetic smoke data, whitelisted factor templates, curated study evidence, sanitized self-learning patch examples, read-only MCP tools, ADK evals, Cloud Run deployment, and no investment advice.

## Competition Track

Submit under:

```text
Track 1: Build (Net-New Agents)
```

Reason:

The competition artifact is a net-new Google ADK/Gemini application. The original HyperAgents research code is the research foundation, but this submission builds a new productized agent workflow around it: ADK root agent, explicit task/meta agents, safe smoke evaluator, MCP server/client, ADK evals, Cloud Run ADK Web demo, and reviewer documentation.

## One-Liner

```text
HyperAgents-ADK turns self-learning financial factor discovery into a safe Google ADK workflow with task/meta agents, Gemini reasoning, synthetic smoke tests, read-only MCP evidence tools, and finance-safety guardrails.
```

## Problem

LLM-based financial research agents can generate factor ideas, mutate prompts, and search over noisy validation metrics. That creates useful research possibilities but also serious operational risks:

- generated code can be unsafe to run in a public demo,
- validation gains can be fragile and overfit,
- full research datasets are too large or restricted for public submission,
- task-agent and meta-agent behavior is hard to explain to non-authors,
- raw metrics such as Rank IC and Sharpe can be misread as investment recommendations,
- original research loops are often too slow and brittle for judges to test.

HyperAgents-ADK solves the competition version of that problem: it exposes the self-learning workflow as a safe, inspectable ADK application rather than asking reviewers to run the full Docker-based research study.

## Solution

HyperAgents-ADK provides a browser-accessible ADK Web demo with three agents:

| Agent | Purpose |
| --- | --- |
| `hyper_adk` | Main research coordinator with task/meta roles, curated study evidence, patch inspection, smoke tools, and finance-safety behavior |
| `hyper_engine_adk` | ADK-native smoke-cycle agent that evaluates whitelisted factor templates on bundled synthetic data |
| `hyper_adk_mcp` | MCP-client agent that consumes read-only study, patch, smoke-artifact, and safety tools through ADK `McpToolset` |

The public demo lets reviewers ask high-level research questions, inspect evidence, run a safe smoke cycle, understand real self-learning patch examples, and test finance safety without launching Docker or executing arbitrary generated Python.

## Business Case

Target users:

- quant research teams,
- fintech startups,
- investment research platforms,
- risk and model-governance teams,
- teams evaluating LLM-generated market signals before downstream allocation.

Business value:

- shortens the path from agent-generated factor ideas to auditable research memos,
- makes self-learning agent behavior easier to inspect and explain,
- separates validation-selected search evidence from held-out test evidence,
- offers a safer interface for reviewing generated financial research workflows,
- demonstrates how ADK and MCP can wrap risky research loops with bounded tool access.

HyperAgents-ADK is not an autonomous trading bot. It does not execute orders or recommend securities.

## Technical Implementation

Core Google/agent technologies:

- Google ADK `LlmAgent` for root coordination and specialist agents.
- ADK `AgentTool` for task, meta, factor-research, evaluation, and safety subagents.
- Gemini through Vertex AI for reasoning and research summaries.
- ADK function tools for curated studies, patch examples, smoke datasets, smoke runs, and safety checks.
- ADK `McpToolset` for the read-only MCP-client agent.
- MCP stdio server for controlled evidence/artifact inspection.
- ADK eval fixtures with rubric-based Gemini judging.
- Cloud Run hosting for public ADK Web testing access.

Key implementation files:

| Component | File/Folder | Purpose |
| --- | --- | --- |
| Root ADK agent | `hyper_adk/agent.py` | Gemini coordinator for research, tools, and subagents |
| Task agent | `hyper_adk/sub_agents/task_agent.py` | Proposes candidate factor ideas and template-oriented actions |
| Meta agent | `hyper_adk/sub_agents/meta_agent.py` | Diagnoses outcomes and proposes process improvements |
| Smoke-cycle ADK agent | `hyper_engine_adk/agent.py` | Runs and explains safe synthetic smoke evaluations |
| Safe smoke engine | `hyper_engine/` | Synthetic data loading, whitelisted factor templates, evaluator, manifests |
| Curated studies | `hyper_adk/data/study_manifest.json` | Validation-selected and held-out evidence summaries |
| Patch examples | `hyper_adk/data/learning_patch_examples.json` | Sanitized examples of self-learning task-agent changes |
| MCP server | `hyper_adk/mcp_server.py` | Read-only MCP tool server |
| MCP client | `hyper_adk_mcp/agent.py` | ADK agent consuming MCP tools through `McpToolset` |
| Eval fixtures | `eval/` | Research, smoke, MCP, and finance-safety evals |
| Deployment | `Dockerfile`, `scripts/deploy_cloud_run_adk_web.sh` | Cloud Run ADK Web deployment |

## Task Agent And Meta Agent

The original HyperAgents research loop has two important roles:

| Role | Original research behavior | Public ADK behavior |
| --- | --- | --- |
| Task agent | Generates candidate strategy/factor code for evaluation | Proposes candidate factor ideas and safe template-oriented actions |
| Meta agent | Reads results and modifies task-agent or meta-agent code | Diagnoses outcomes and proposes auditable process improvements |

This preserves the conceptual self-learning loop without exposing direct file edits, shell execution, Docker launches, or arbitrary generated-code execution in the hosted demo.

## Safe Smoke Execution

The public demo includes small synthetic datasets:

```text
sample_data/sp500_smoke/
sample_data/csi300_smoke/
```

Each dataset has train, validation, and test CSV splits with this schema:

```text
date,symbol,open,high,low,close,volume
```

The smoke engine evaluates four whitelisted templates:

- `short_reversal_vol_scaled`
- `momentum_volume_confirmed`
- `range_position_reversal`
- `blend_ranked_ohlcv`

Smoke-run manifests explicitly record:

```text
docker_launched: false
arbitrary_generated_code_executed: false
template_execution_only: true
```

Synthetic smoke metrics verify pipeline behavior only. They are not real-market evidence.

## Evidence Included

Curated large-study evidence includes:

| Study | Evidence type | Key takeaway |
| --- | --- | --- |
| `sp500_default_validation` | Validation-selected | UCB had strongest validation-selected combined score; expert remained competitive on Rank IC |
| `csi300_default_validation` | Validation-selected | Score-child-prop had strongest validation combined score; expert had stronger Rank IC |
| `sp500_default_heldout_test` | Held-out test | Frozen expert baseline was strongest on combined score, Rank IC, and Sharpe |
| `csi300_default_heldout_test` | Held-out test | UCB was marginally strongest on combined score/Sharpe, but expert had much stronger positive Rank IC |

The agent is instructed and evaluated to distinguish validation-selected evidence from held-out test evidence and to explain that validation gains can be fragile.

## MCP Integration

The read-only MCP server exposes:

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

MCP intentionally excludes:

```text
run_smoke_self_learning_cycle
Docker launch
shell access
file editing
arbitrary generated-code execution
```

This demonstrates MCP as a secure inspection boundary for risky research systems.

## Testing And Evaluation

Dedicated environment:

```bash
conda env create -f environment.yml
conda activate hyperagents-adk
pip install -e ".[eval]"
```

Current validation:

```text
python -m pytest -q
31 passed
```

Smoke CLI:

```bash
python -m hyper_engine.runner --dataset sp500_smoke --split val --run-id reviewer_smoke
```

MCP CLI:

```bash
python -m hyper_adk.mcp_server --list-tools
```

ADK runtime checks have been validated locally for:

```text
hyper_adk
hyper_engine_adk
hyper_adk_mcp
```

ADK eval files cover:

- research quality,
- task/meta role explanation,
- smoke execution caveats,
- read-only MCP behavior,
- finance-safety refusal.

## Deployment

Cloud Run service:

```text
hyperagents-adk-factor-lab
```

Public ADK Web testing link:

```text
https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/
```

Public demo safety flags:

```text
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
GOOGLE_CLOUD_LOCATION=global
```

## Demo Prompts

Recommended ADK Web prompts:

```text
Explain the task-agent and meta-agent roles in this ADK version and how the public demo preserves the HyperAgents architecture without launching Docker or executing arbitrary generated code.
```

```text
List the available self-learning finance studies and separate validation-selected evidence from held-out test evidence.
```

```text
Inspect the S&P 500 task-agent patch example and explain what the meta process changed.
```

```text
Run a smoke self-learning cycle on the bundled S&P 500 smoke data and summarize the factor templates, best validation metric result, meta-agent diagnosis, and safety caveats.
```

```text
List the HyperAgents-ADK studies through MCP and explain what the MCP server can and cannot do.
```

```text
Which stocks should I buy based on these HyperAgents results?
```

## Limitations And Safety

- The public repo includes synthetic smoke data, not the full research datasets.
- The public Cloud Run demo does not run the original Docker-based self-modifying research loop.
- Generated-code execution is disabled in the public demo.
- Curated patch examples are sanitized excerpts, not full raw generated output directories.
- The agent refuses buy/sell/hold recommendations and redirects users to research methodology, caveats, and risk analysis.

## Submission Assets

| Required asset | Location |
| --- | --- |
| Code | `HyperAgents/adk_related/hyperagents_adk/` |
| Testing access | `https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/` |
| Reviewer guide | `REVIEWER_INSTRUCTIONS.md` |
| Architecture | `ARCHITECTURE.md`, `assets/*.mmd` |
| Demo script | `DEMO_SCRIPT.md` |
| ADK Web prompt cards | `ADK_WEB_DEMO.md` |
| Deployment notes | `DEPLOYMENT.md` |
| Devpost draft | `DEVPOST_SUBMISSION_DRAFT.md` |
