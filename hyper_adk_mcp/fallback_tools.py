"""Read-only fallback tools for hosted ADK Web MCP demos.

The primary MCP integration remains `hyper_adk.mcp_server` plus ADK `McpToolset`.
Cloud Run can occasionally fail to start the stdio MCP subprocess quickly enough
inside ADK Web. These fallback tools mirror the same read-only functions so the
hosted demo remains reliable without exposing execution, Docker, shell, or file
editing capabilities.
"""

from __future__ import annotations

from typing import Any

from hyper_adk.tools import (
    compare_conditions,
    explain_task_meta_roles,
    finance_safety_check,
    get_study_summary,
    inspect_learning_patch,
    inspect_smoke_engine_run,
    list_available_studies,
    list_learning_patch_examples,
    list_smoke_datasets,
    list_smoke_engine_runs,
)


def mcp_fallback_list_available_studies(
    dataset: str | None = None,
    evidence_type: str | None = None,
) -> dict[str, Any]:
    """Fallback mirror of the read-only MCP study-listing tool."""

    return list_available_studies(dataset=dataset, evidence_type=evidence_type)


def mcp_fallback_get_study_summary(study_id: str) -> dict[str, Any]:
    """Fallback mirror of the read-only MCP study-summary tool."""

    return get_study_summary(study_id=study_id)


def mcp_fallback_compare_conditions(
    study_id: str,
    primary_metric: str = "combined_score_mean",
) -> dict[str, Any]:
    """Fallback mirror of the read-only MCP study-comparison tool."""

    return compare_conditions(study_id=study_id, primary_metric=primary_metric)


def mcp_fallback_list_learning_patch_examples(
    dataset: str | None = None,
    agent_modified: str | None = None,
) -> dict[str, Any]:
    """Fallback mirror of the read-only MCP patch-listing tool."""

    return list_learning_patch_examples(dataset=dataset, agent_modified=agent_modified)


def mcp_fallback_inspect_learning_patch(example_id: str) -> dict[str, Any]:
    """Fallback mirror of the read-only MCP patch-inspection tool."""

    return inspect_learning_patch(example_id=example_id)


def mcp_fallback_explain_task_meta_roles() -> dict[str, Any]:
    """Fallback mirror of the read-only MCP task/meta role tool."""

    return explain_task_meta_roles()


def mcp_fallback_list_smoke_datasets() -> dict[str, Any]:
    """Fallback mirror of the read-only MCP smoke-dataset listing tool."""

    return list_smoke_datasets()


def mcp_fallback_list_smoke_engine_runs() -> dict[str, Any]:
    """Fallback mirror of the read-only MCP smoke-run listing tool."""

    return list_smoke_engine_runs()


def mcp_fallback_inspect_smoke_engine_run(run_id: str) -> dict[str, Any]:
    """Fallback mirror of the read-only MCP smoke-run inspection tool."""

    return inspect_smoke_engine_run(run_id=run_id)


def mcp_fallback_finance_safety_check(user_request: str) -> dict[str, object]:
    """Fallback mirror of the read-only MCP finance-safety tool."""

    return finance_safety_check(user_request=user_request)
