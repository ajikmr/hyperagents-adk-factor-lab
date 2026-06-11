"""Placeholder tools for the smoke-cycle ADK agent."""

from __future__ import annotations

from hyper_adk.config import load_config
from hyper_adk.tools.smoke_tools import (
    inspect_smoke_engine_run,
    list_smoke_datasets,
    list_smoke_engine_runs,
    run_smoke_self_learning_cycle,
)


def describe_smoke_engine_status() -> dict[str, object]:
    """Describe the current smoke-engine implementation status."""

    config = load_config()
    return {
        "status": "skeleton",
        "implemented_now": [
            "project configuration",
            "ADK package structure",
            "curated study manifest",
            "study-inspection tools",
        ],
        "next_engine_milestone": [
            "synthetic smoke data",
            "safe factor templates",
            "cross-sectional smoke evaluator",
            "local artifact manifests",
        ],
        "default_dataset": config.default_dataset,
        "live_runs_enabled": config.enable_live_runs,
        "generated_code_enabled": config.enable_generated_code,
    }


__all__ = [
    "describe_smoke_engine_status",
    "inspect_smoke_engine_run",
    "list_smoke_datasets",
    "list_smoke_engine_runs",
    "run_smoke_self_learning_cycle",
]
