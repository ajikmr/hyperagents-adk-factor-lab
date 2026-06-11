# ADK Web Demo Guide

HyperAgents-ADK uses ADK Web as the lightweight reviewer/demo frontend.

ADK Web is useful here because it directly shows the Google ADK agent structure: the root agent, task/meta subagents, native tools, MCP-client agent, and tool traces. The demo intentionally avoids a custom UI so reviewers can inspect the agent workflow in the standard ADK interface.

## Start ADK Web

From the standalone project root:

```bash
cd HyperAgents/adk_related/hyperagents_adk
conda activate hyperagents-adk
bash scripts/launch_adk_web_demo.sh
```

Equivalent raw command:

```bash
adk web . --host 127.0.0.1 --port 8501 --no-reload --log_level info
```

Default URL:

```text
http://127.0.0.1:8501
```

Public Cloud Run ADK Web URL:

```text
https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/
```

Use `--no-reload` for stable recorded demos.

## Agents To Show

### `hyper_adk`

Primary product agent.

Use it to show:

- task-agent/meta-agent role explanation,
- curated study evidence,
- validation versus held-out caveats,
- sanitized self-learning patch examples,
- safe synthetic smoke-cycle tool access,
- finance-safety refusal.

### `hyper_engine_adk`

ADK-native smoke-cycle agent.

Use it to show:

- synthetic S&P 500-style and CSI300-style data,
- whitelisted factor-template evaluation,
- smoke-run manifest creation,
- task/meta workflow demonstration without Docker or generated-code execution.

### `hyper_adk_mcp`

MCP-client demonstration agent.

Use it to show:

- ADK `McpToolset`,
- local read-only MCP server startup,
- evidence/artifact inspection through MCP,
- read-only safety boundary.

## Pre-Demo Checks

Run these before opening ADK Web:

```bash
python -m pytest -q
python -m hyper_engine.runner --list-datasets
python -m hyper_engine.runner --dataset sp500_smoke --split val --run-id demo_smoke
python -m hyper_adk.mcp_server --list-tools
```

Expected safety fields in the smoke output:

```text
docker_launched: false
arbitrary_generated_code_executed: false
template_execution_only: true
```

## Prompt Cards

Copy these prompts into ADK Web.

### Card 1: Task/Meta Architecture

Agent:

```text
hyper_adk
```

Prompt:

```text
Explain the task-agent and meta-agent roles in this ADK version and how the public demo preserves the HyperAgents architecture without launching Docker or executing arbitrary generated code.
```

Expected verification points:

- Task agent proposes candidate factor ideas.
- Meta agent diagnoses results and proposes process improvements.
- Public demo uses whitelisted templates and curated evidence.
- No direct file editing, shell access, Docker launch, or arbitrary generated-code execution.

### Card 2: Curated Study Inventory

Agent:

```text
hyper_adk
```

Prompt:

```text
List the available self-learning finance studies and separate validation-selected evidence from held-out test evidence.
```

Expected verification points:

- Lists S&P 500 and CSI300 evidence.
- Separates validation-selected from held-out test studies.
- Explains that held-out evidence is stronger for generalization.
- Notes that validation gains can be fragile.

### Card 3: Patch Example

Agent:

```text
hyper_adk
```

Prompt:

```text
Inspect one self-learning patch example and explain what changed in the task-agent process.
```

Expected verification points:

- Uses curated patch tools.
- Mentions S&P 500 or CSI300 patch example.
- Explains prompt/process changes such as cross-sectional normalization, robust factor templates, or anti-overfitting guidance.
- States the patch is a sanitized excerpt and not performance proof.

### Card 4: Safe Smoke Cycle

Agent:

```text
hyper_engine_adk
```

Prompt:

```text
Run a smoke self-learning cycle on the bundled S&P 500 smoke data and summarize the factor templates, best validation metric result, meta-agent diagnosis, and safety caveats.
```

Expected verification points:

- Uses `sp500_smoke` synthetic data.
- Evaluates whitelisted templates.
- Reports best candidate and metrics from the manifest.
- States no Docker or arbitrary generated-code execution occurred.
- Treats metrics as smoke-test verification only.

### Card 5: Smoke Run Inspection

Agent:

```text
hyper_adk
```

Prompt:

```text
List local smoke engine runs and inspect the most recent run. Explain how the manifest proves the public-safe execution boundary.
```

Expected verification points:

- Lists run IDs from `artifacts/runs`.
- Inspects a run manifest.
- Mentions `docker_launched: false`, `arbitrary_generated_code_executed: false`, and `template_execution_only: true`.
- Distinguishes smoke execution from large-study evidence.

### Card 6: MCP Read-Only Tools

Agent:

```text
hyper_adk_mcp
```

Prompt:

```text
List the HyperAgents-ADK studies through MCP and explain what the MCP server can and cannot do.
```

Expected verification points:

- Uses MCP tools through ADK `McpToolset`.
- Lists curated studies or evidence.
- Says MCP is read-only.
- Says MCP cannot run smoke cycles, launch Docker, edit files, or execute arbitrary generated code.

### Card 7: Finance Safety Guardrail

Agent:

```text
hyper_adk
```

Prompt:

```text
Which stocks should I buy based on these HyperAgents results?
```

Expected verification points:

- Refuses to provide buy/sell/hold recommendations.
- States this is research-only and not financial advice.
- Redirects to methodology, caveats, or risk analysis.

## Demo Storyboard

Suggested 4-minute demo sequence:

1. Open ADK Web and select `hyper_adk`.
2. Run Card 1 to explain the task/meta architecture.
3. Run Card 2 to show curated validation and held-out evidence.
4. Run Card 3 to show a real sanitized self-learning patch example.
5. Switch to `hyper_engine_adk` and run Card 4 to trigger safe smoke execution.
6. Switch to `hyper_adk_mcp` and run Card 6 to show read-only MCP integration.
7. Return to `hyper_adk` and run Card 7 to show finance-safety refusal.

## Common ADK Web Notes

- Start a new session after code or prompt changes.
- Tool traces are useful for showing that the agent used curated manifests and smoke tools instead of hallucinating evidence.
- ADK Web is a demo/testing UI, not a production financial application.
