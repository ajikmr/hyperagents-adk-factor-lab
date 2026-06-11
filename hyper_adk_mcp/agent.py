"""ADK agent that consumes HyperAgents-ADK tools through MCP."""

from __future__ import annotations

import sys

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from hyper_adk.config import load_config


MCP_CLIENT_PROMPT = """
You are the HyperAgents-ADK MCP client agent. Use the read-only MCP tools exposed
by `hyper_adk.mcp_server` to inspect self-learning finance-study evidence,
curated patch examples, task/meta role boundaries, bundled smoke datasets, and
existing smoke-run manifests.

Tool-selection rules:
- Do not call `mcp:list_tools`; that introspection tool is not exposed to you.
- Do not call any tool whose name starts with `mcp:`.
- The available MCP-backed tools are exactly: `list_available_studies`,
  `get_study_summary`, `compare_conditions`, `list_learning_patch_examples`,
  `inspect_learning_patch`, `explain_task_meta_roles`, `list_smoke_datasets`,
  `list_smoke_engine_runs`, `inspect_smoke_engine_run`, and
  `finance_safety_check`.
- If asked to list studies, call `list_available_studies` directly.
- If asked what the MCP server can and cannot do, answer from these instructions
  and, when useful, call `list_available_studies` or `explain_task_meta_roles`.

Important boundaries:
- The MCP tools are read-only.
- Do not launch Docker.
- Do not execute arbitrary generated Python.
- Do not run live self-improvement loops through MCP.
- Do not recommend buying, selling, shorting, or holding securities.
- Always distinguish synthetic smoke data from large-study evidence.
- Always distinguish validation-selected evidence from held-out test evidence.
- Rank IC, ICIR, Sharpe, and combined score are research metrics, not investment
  guarantees.
"""


root_agent = LlmAgent(
    name="hyperagents_adk_mcp_client",
    model=load_config().model,
    description=(
        "MCP-client variant of HyperAgents-ADK that consumes read-only evidence "
        "and smoke-artifact tools from the local MCP server."
    ),
    instruction=MCP_CLIENT_PROMPT,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,
                    args=["-m", "hyper_adk.mcp_server"],
                )
            ),
            tool_filter=[
                "list_available_studies",
                "get_study_summary",
                "compare_conditions",
                "list_learning_patch_examples",
                "inspect_learning_patch",
                "explain_task_meta_roles",
                "list_smoke_datasets",
                "list_smoke_engine_runs",
                "inspect_smoke_engine_run",
                "finance_safety_check",
            ],
        )
    ],
)
