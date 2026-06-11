# HyperAgents-ADK Demo Script

This script is intended for a 3-5 minute competition video or live reviewer walkthrough.

Run commands from:

```bash
cd HyperAgents/adk_related/hyperagents_adk
conda activate hyperagents-adk
```

Use ADK Web as the frontend for the recorded demo:

```bash
bash scripts/launch_adk_web_demo.sh
```

Open `http://127.0.0.1:8501` and follow the prompt cards in `ADK_WEB_DEMO.md`.

## Setup Check

Narration:

```text
HyperAgents-ADK is a Track 1 net-new Google ADK application for self-learning financial factor research. It preserves the HyperAgents task-agent and meta-agent architecture while making the public demo safe: synthetic data, whitelisted templates, curated evidence, read-only MCP, and no investment advice.
```

Command:

```bash
python -m pytest -q
```

Expected:

```text
19 passed
```

## Scene 1: Architecture

Narration:

```text
The core architecture has two main agents. The task agent proposes candidate factor ideas. The meta agent diagnoses results and proposes improvements to the process. The public ADK version does not expose the original Docker loop; it uses safe tools and manifests instead.
```

Show:

- `ARCHITECTURE.md` high-level diagram.
- `hyper_adk/sub_agents/task_agent.py`.
- `hyper_adk/sub_agents/meta_agent.py`.
- Safety boundaries in `DEPLOYMENT.md`.

## Scene 2: Task/Meta Role Explanation

Agent:

```text
hyper_adk
```

Prompt:

```text
Explain the task-agent and meta-agent roles in this ADK version and how the public demo preserves the HyperAgents architecture without launching Docker or executing arbitrary generated code.
```

Show:

- Task agent proposes candidates.
- Meta agent diagnoses and improves process.
- Public demo uses whitelisted templates and curated evidence.
- No Docker or arbitrary generated-code execution.

## Scene 3: Curated Study Evidence

Agent:

```text
hyper_adk
```

Prompt:

```text
List the available self-learning finance studies and separate validation-selected evidence from held-out test evidence.
```

Show:

- S&P 500 and CSI300 evidence.
- Validation-selected studies versus held-out test studies.
- Generalization fragility caveat.
- Research-only framing.

## Scene 4: Self-Learning Patch Example

Agent:

```text
hyper_adk
```

Prompt:

```text
Inspect the S&P 500 task-agent patch example and explain what the meta process changed.
```

Show:

- Robust factor-family guidance.
- Cross-sectional normalization.
- Fallback behavior.
- Anti-overfitting guidance.
- Sanitized excerpt caveat.

## Scene 5: Safe Smoke Execution

Agent:

```text
hyper_engine_adk
```

Prompt:

```text
Run a smoke self-learning cycle on the bundled S&P 500 smoke data and summarize the factor templates, best validation metric result, meta-agent diagnosis, and safety caveats.
```

Show:

- Synthetic `sp500_smoke` data.
- Four whitelisted templates.
- Best candidate and metrics.
- `docker_launched: false`.
- `arbitrary_generated_code_executed: false`.
- `template_execution_only: true`.

Optional CLI cutaway:

```bash
python -m hyper_engine.runner --dataset sp500_smoke --split val --run-id video_smoke
```

## Scene 6: Read-Only MCP

Narration:

```text
For safe interoperability, HyperAgents-ADK also exposes read-only evidence tools through MCP. The MCP server can inspect studies, patch examples, datasets, and run manifests, but it cannot trigger execution.
```

Command:

```bash
python -m hyper_adk.mcp_server --list-tools
```

Agent:

```text
hyper_adk_mcp
```

Prompt:

```text
List the HyperAgents-ADK studies through MCP and explain what the MCP server can and cannot do.
```

Show:

- ADK `McpToolset` client.
- Read-only tool list.
- No `run_smoke_self_learning_cycle` through MCP.
- No Docker, file editing, or generated-code execution.

## Scene 7: Finance Safety Guardrail

Agent:

```text
hyper_adk
```

Prompt:

```text
Which stocks should I buy based on these HyperAgents results?
```

Show:

- No buy/sell/hold recommendation.
- Research-only disclaimer.
- Safe alternative: methodology, caveats, or evaluation risk.

## Scene 8: ADK Eval Mention

Narration:

```text
The repository includes ADK eval fixtures for research quality, smoke execution, MCP read-only behavior, and finance safety. These evals check that the agent stays grounded in tools and preserves the public execution boundary.
```

Example commands after ADK dependencies and credentials are configured:

```bash
adk eval hyper_adk eval/data/hyper_adk_research.test.json \
  --config_file_path eval/research_eval_config.json

adk eval hyper_engine_adk eval/data/hyper_adk_smoke.test.json \
  --config_file_path eval/smoke_eval_config.json

adk eval hyper_adk eval/data/hyper_adk_safety.test.json \
  --config_file_path eval/safety_eval_config.json

adk eval hyper_adk_mcp eval/data/hyper_adk_mcp.test.json \
  --config_file_path eval/mcp_eval_config.json
```

## Closing Line

```text
HyperAgents-ADK turns a brittle full research loop into a judge-testable Google ADK application: task/meta agents, safe smoke execution, curated evidence, read-only MCP, and finance-safe explanations.
```
