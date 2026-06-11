# Presentation Strategy

This document maps the Google for Startups AI Agents Challenge criteria to how HyperAgents-ADK should be presented.

## Positioning

Use this framing:

```text
HyperAgents-ADK is a Track 1 net-new Google ADK application that turns self-learning financial factor discovery into a safe, auditable research workflow with task/meta agents, Gemini reasoning, synthetic smoke execution, read-only MCP tools, and finance-safety guardrails.
```

Avoid this framing:

```text
An AI trading bot that finds stocks to buy.
```

The latter creates regulatory risk and misrepresents the system.

## Challenge Criteria Mapping

| Criterion | What To Emphasize | Demo Moment |
| --- | --- | --- |
| Technical Implementation (30%) | ADK root agent, task/meta subagents, Gemini, tools, MCP, evals, Cloud Run | Architecture diagram, ADK Web, MCP prompt |
| Business Case (30%) | Safer research workflow for quant/fintech teams evaluating LLM-generated factors | Problem framing and validation-vs-held-out caveat |
| Innovation & Creativity (20%) | Self-learning task/meta architecture adapted into a bounded public agent | Patch example and meta-agent diagnosis |
| Demo & Presentation (20%) | Hosted ADK Web, smoke execution, read-only MCP, no-advice refusal | Prompt cards from `ADK_WEB_DEMO.md` |

## Best Opening For Video

Use a direct before/after contrast:

```text
Self-learning financial agents can generate and improve factor ideas, but the original research loop is not safe or practical as a public demo: it can execute generated code, launch Docker, and overfit noisy validation metrics.

HyperAgents-ADK turns that research concept into a new Google ADK application. Reviewers can inspect curated studies, run a synthetic smoke cycle, see task-agent and meta-agent roles, query read-only MCP tools, and verify finance-safety behavior in Cloud Run ADK Web.
```

## What To Show

Recommended sequence:

1. Public Cloud Run ADK Web URL.
2. Architecture diagram from `ARCHITECTURE.md`.
3. `hyper_adk` explaining task-agent and meta-agent roles.
4. Curated study inventory separating validation-selected and held-out evidence.
5. Sanitized S&P 500 or CSI300 self-learning patch example.
6. `hyper_engine_adk` running safe synthetic smoke execution.
7. Smoke manifest safety fields: `docker_launched: false`, `arbitrary_generated_code_executed: false`, `template_execution_only: true`.
8. `hyper_adk_mcp` listing studies through read-only MCP.
9. Finance-safety prompt refusing stock recommendations.
10. Test baseline: `31 passed`.

## What To Avoid

- Do not call it a trading bot.
- Do not recommend securities.
- Do not claim synthetic smoke metrics prove real performance.
- Do not imply the public repo reproduces the full paper-scale study.
- Do not run the original Docker loop live in the public demo.
- Do not overstate validation-selected results as held-out generalization.
- Do not show `.env`, credentials, service-account files, or private datasets.

## Submission Page Copy

Suggested short description:

```text
HyperAgents-ADK Self-Learning Factor Lab is a Google ADK and Gemini-powered financial research agent for safe self-learning factor discovery. It coordinates task and meta agents, runs synthetic smoke evaluations through whitelisted factor templates, inspects curated validation and held-out study evidence, exposes read-only MCP tools, and enforces finance-safety guardrails so reviewers can audit agentic factor research without executing arbitrary generated code.
```

Suggested built-with list:

```text
Google ADK, Gemini 3.5 Flash via Vertex AI, ADK Web, ADK Eval, MCP, Cloud Run, Python, Conda, pandas, scipy, synthetic OHLCV data, pytest.
```

Suggested tagline:

```text
Safe self-learning financial factor research with Google ADK, Gemini, MCP, and synthetic smoke tests.
```

## Testing Access Copy

```text
Public Cloud Run ADK Web demo: https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/

Select one of the agents from the dropdown: hyper_adk, hyper_engine_adk, or hyper_adk_mcp. The public demo uses bundled synthetic smoke data and keeps live self-improvement plus generated-code execution disabled.
```

## Suggested Prompt Cards

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

## Visual Assets To Produce

Existing sources:

```text
assets/architecture.mmd
assets/native_adk_flow.mmd
assets/mcp_flow.mmd
ARCHITECTURE.md
```

Before final submission, render or capture:

1. `assets/architecture.png`.
2. `assets/native_adk_flow.png`.
3. `assets/mcp_flow.png`.
4. ADK Web screenshot with `hyper_adk`, `hyper_engine_adk`, and `hyper_adk_mcp` visible.
5. Screenshot of `hyper_engine_adk` smoke run response.
6. Screenshot of `hyper_adk_mcp` MCP study listing response.
7. Screenshot of finance-safety refusal.

## Final Checklist

- `README.md` gives setup, public demo URL, and key docs.
- `SUBMISSION.md` explains project, architecture, safety, and evidence.
- `DEVPOST_SUBMISSION_DRAFT.md` has copy-ready submission text.
- `ARCHITECTURE.md` documents system flow and safety boundaries.
- `DEMO_SCRIPT.md` supports recording.
- `ADK_WEB_DEMO.md` provides prompt cards.
- `DEPLOYMENT.md` documents local and Cloud Run setup.
- `REVIEWER_INSTRUCTIONS.md` gives commands and pass criteria.
- Cloud Run demo works for all three agents.
- Dedicated `hyperagents-adk` env passes tests.
- No credentials, `.env`, service-account JSON, original full datasets, or generated full output directories are committed.
