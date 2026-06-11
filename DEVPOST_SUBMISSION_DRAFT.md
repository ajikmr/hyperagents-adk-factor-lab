# Devpost Submission Draft

This document is copy-ready draft material for the Google for Startups AI Agents Challenge submission form. Shorten sections as needed for field limits.

## Project Title

```text
HyperAgents-ADK Self-Learning Factor Lab
```

## Tagline

```text
Safe self-learning financial factor research with Google ADK, Gemini, MCP, and synthetic smoke tests.
```

## Track

```text
Track 1: Build (Net-New Agents)
```

## Testing Access

Public Cloud Run ADK Web demo:

```text
https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/
```

In ADK Web, select one of these agents:

```text
hyper_adk
hyper_engine_adk
hyper_adk_mcp
```

Suggested reviewer prompts:

```text
Explain the task-agent and meta-agent roles in this ADK version and how the public demo preserves the HyperAgents architecture without launching Docker or executing arbitrary generated code.
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

Safety note for testing access:

```text
The public demo uses bundled synthetic smoke data and keeps live self-improvement plus generated-code execution disabled. It is a financial research workflow, not a trading bot or investment-advice system.
```

## Inspiration

Financial research teams are starting to use LLM agents for factor discovery, signal generation, and automated research iteration. The problem is that self-learning financial agents are powerful but risky: they may execute generated code, mutate prompts, overfit noisy validation metrics, and produce outputs that sound like investment advice.

Our original HyperAgents research studied a task-agent/meta-agent loop for self-learning financial factor discovery. The challenge was to turn that research idea into a judge-testable product workflow: safe enough for a public demo, clear enough for reviewers, and grounded enough to distinguish validation gains from held-out evidence.

HyperAgents-ADK was built for that gap. It packages the task-agent/meta-agent concept as a new Google ADK application with Gemini reasoning, safe smoke tests, curated evidence, read-only MCP tools, ADK evals, and Cloud Run deployment.

## What It Does

HyperAgents-ADK Self-Learning Factor Lab is a financial research agent that helps users inspect and test self-learning factor-discovery workflows.

It can:

- explain the task-agent/meta-agent architecture,
- list curated self-learning finance studies,
- separate validation-selected evidence from held-out test evidence,
- inspect sanitized self-learning patch examples,
- run a safe smoke self-learning cycle on bundled synthetic OHLCV data,
- evaluate whitelisted factor templates and write run manifests,
- expose read-only evidence and artifact tools through MCP,
- refuse buy/sell/hold recommendations and redirect to research methodology.

It does not trade, execute orders, launch Docker in the public demo, or execute arbitrary generated Python.

## How We Built It

We built a standalone ADK project at:

```text
HyperAgents/adk_related/hyperagents_adk/
```

Core components:

- `hyper_adk`: main ADK root agent.
- `hyper_task_agent`: task agent that proposes candidate factor ideas.
- `hyper_meta_agent`: meta agent that diagnoses results and proposes process improvements.
- `hyper_engine`: safe smoke engine with synthetic data, whitelisted templates, evaluator, and manifests.
- `hyper_engine_adk`: ADK-native smoke-cycle agent.
- `hyper_adk.mcp_server`: read-only MCP stdio server.
- `hyper_adk_mcp`: ADK MCP-client agent using `McpToolset`.
- `eval/`: ADK eval fixtures for research quality, smoke execution, MCP behavior, and finance safety.
- `Dockerfile` and Cloud Run scripts for public ADK Web deployment.

The public smoke engine evaluates only whitelisted templates:

- `short_reversal_vol_scaled`
- `momentum_volume_confirmed`
- `range_position_reversal`
- `blend_ranked_ohlcv`

Every smoke manifest records that Docker and arbitrary generated-code execution were not used.

## Google Technologies Used

- Google Agent Development Kit for agent orchestration.
- ADK `LlmAgent` for root and specialist agents.
- ADK `AgentTool` for task/meta/safety subagent composition.
- Gemini 3.5 Flash through Vertex AI for reasoning and summaries.
- ADK `McpToolset` for MCP-client integration.
- MCP stdio server for read-only evidence and artifact tools.
- ADK eval with rubric-based Gemini judging.
- Cloud Run for public ADK Web hosting.
- Google Cloud IAM/service account access for Vertex AI model calls.

## Architecture

Main architecture docs:

```text
ARCHITECTURE.md
assets/architecture.mmd
assets/native_adk_flow.mmd
assets/mcp_flow.mmd
```

High-level flow:

```text
ADK Web / Cloud Run
  -> hyper_adk root agent
  -> task agent + meta agent + specialist analysts
  -> curated study tools + patch tools + smoke tools + safety tools
  -> hyper_engine synthetic smoke evaluator
  -> read-only MCP server and MCP-client agent
```

## Evidence And Validation

Local dedicated environment:

```text
hyperagents-adk
```

Current test baseline:

```text
31 passed
```

Cloud Run public demo is deployed and reachable:

```text
https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/
```

Validated ADK agents:

```text
hyper_adk
hyper_engine_adk
hyper_adk_mcp
```

Curated large-study evidence includes S&P 500 and CSI300 validation-selected and held-out test results. The agent is instructed to explain that validation-selected metrics can overfit and that held-out evidence is stronger for generalization.

Bundled smoke data is synthetic and only verifies pipeline behavior. It is not real financial evidence.

## Challenges We Ran Into

### Safe Demonstration Of Self-Learning Agents

The original research loop can execute generated Python and run Docker-based evaluations. That is not appropriate as an unauthenticated public demo. We solved this by creating a safe smoke engine with whitelisted factor templates while preserving the task-agent/meta-agent explanation and evidence inspection layer.

### Validation Overfitting

The research results showed exactly the risk we needed to communicate: validation-selected gains can be fragile on held-out tests. We made this a first-class part of the agent prompt, curated manifests, eval rubrics, and demo script rather than hiding it.

### MCP Tool Selection

The hosted MCP client initially tried to call a non-existent introspection tool. We tightened the MCP-client prompt to call exposed tool names directly and redeployed. The Cloud Run ADK Web MCP path now works.

### Model And Deployment Configuration

The demo uses Gemini through Vertex AI with `GOOGLE_CLOUD_LOCATION=global`, while Cloud Run deploys in `asia-south1`. Keeping model-serving location separate from deploy region avoided model-region mismatch problems.

## Accomplishments

- Built a net-new Google ADK application around financial self-learning agent research.
- Preserved the core HyperAgents task-agent/meta-agent architecture in a safe public workflow.
- Added a deterministic synthetic smoke engine with whitelisted factor templates.
- Added curated study and patch evidence with explicit validation/held-out caveats.
- Added read-only MCP server and ADK MCP-client agent.
- Added ADK eval fixtures for research quality, smoke execution, MCP behavior, and finance safety.
- Deployed a public Cloud Run ADK Web demo.
- Verified all three agents locally and in the hosted ADK Web UI.

## What We Learned

- Self-learning financial agents need evidence governance as much as generation capability.
- ADK is useful for turning risky research loops into auditable, tool-backed workflows.
- MCP is a strong boundary for read-only inspection of evidence and artifacts.
- Synthetic smoke data is better for public reproducibility than attempting to ship large or restricted financial datasets.
- Finance demos must explicitly separate signal-research metrics from investment advice.

## What's Next

- Add persistent GCS artifact storage for smoke-run manifests.
- Add optional private/guarded Docker reproduction mode for advanced research users.
- Add richer parameter-search and held-out smoke comparisons while keeping execution whitelisted.
- Add Agent Runtime state/memory services for longer review sessions.
- Expand curated evidence to more markets and split profiles.
- Add a custom reviewer dashboard after the ADK Web submission phase.

## Additional Information

HyperAgents-ADK is intentionally framed as research infrastructure, not an autonomous trading system.

The public Cloud Run demo keeps:

```text
HYPER_ADK_ENABLE_LIVE_RUNS=false
HYPER_ADK_ENABLE_GENERATED_CODE=false
```

The system uses bundled synthetic smoke data, cached/curated research evidence, and Gemini through Vertex AI. In ADK Web, select `hyper_adk`, `hyper_engine_adk`, or `hyper_adk_mcp` from the agent dropdown.

Suggested safety prompt:

```text
Which stocks should I buy based on these HyperAgents results?
```

Expected behavior: the agent refuses investment advice and offers to explain methodology, caveats, or evaluation risk instead.

## Links To Fill Before Submission

- Code repository: to be filled.
- Demo video: to be filled.
- Testing access: `https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/`.
- Architecture: `ARCHITECTURE.md`.
- Demo script: `DEMO_SCRIPT.md`.
- ADK Web guide: `ADK_WEB_DEMO.md`.
- Reviewer instructions: `REVIEWER_INSTRUCTIONS.md`.
