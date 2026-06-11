"""Curated self-learning patch inspection tools."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATCH_EXAMPLES_PATH = APP_ROOT / "data" / "learning_patch_examples.json"


@lru_cache(maxsize=4)
def _load_patch_examples_cached(path: str) -> dict[str, Any]:
    patch_path = Path(path)
    with patch_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_patch_examples(path: str | Path | None = None) -> dict[str, Any]:
    """Load curated self-learning patch examples."""

    patch_path = Path(path) if path is not None else DEFAULT_PATCH_EXAMPLES_PATH
    return _load_patch_examples_cached(str(patch_path.resolve()))


def list_learning_patch_examples(
    dataset: str | None = None,
    agent_modified: str | None = None,
) -> dict[str, Any]:
    """List curated self-learning patch examples.

    Args:
        dataset: Optional dataset filter, such as "sp500" or "csi300".
        agent_modified: Optional role filter, such as "task_agent" or
            "meta_agent".
    """

    payload = load_patch_examples()
    examples = []
    for example in payload.get("examples", []):
        if dataset and example.get("dataset", "").lower() != dataset.lower():
            continue
        if agent_modified and example.get("agent_modified", "").lower() != agent_modified.lower():
            continue
        examples.append(
            {
                "id": example["id"],
                "label": example["label"],
                "dataset": example["dataset"],
                "market": example["market"],
                "agent_modified": example["agent_modified"],
                "generation": example["generation"],
                "change_type": example["change_type"],
                "task_agent_effect": example["task_agent_effect"],
                "evaluation_lesson": example["evaluation_lesson"],
            }
        )

    return {
        "examples": examples,
        "count": len(examples),
        "filters": {"dataset": dataset, "agent_modified": agent_modified},
        "global_caveats": payload.get("global_caveats", []),
    }


def inspect_learning_patch(example_id: str) -> dict[str, Any]:
    """Inspect one sanitized self-learning patch example.

    Args:
        example_id: Patch example ID from `list_learning_patch_examples`.
    """

    payload = load_patch_examples()
    for example in payload.get("examples", []):
        if example.get("id") == example_id:
            return {
                **example,
                "global_caveats": payload.get("global_caveats", []),
                "sanitization_note": (
                    "This example is a curated excerpt. Cache files, binary diffs, "
                    "full chat logs, credentials, and full datasets are excluded."
                ),
            }
    available = [example.get("id") for example in payload.get("examples", [])]
    raise ValueError(f"Unknown example_id '{example_id}'. Available examples: {available}")


def explain_task_meta_roles() -> dict[str, Any]:
    """Explain how task-agent and meta-agent roles map into this ADK project."""

    return {
        "task_agent": {
            "original_role": (
                "Generate candidate finance strategies or factor code for evaluation."
            ),
            "adk_role": (
                "Propose candidate factor ideas and safe template-oriented research "
                "actions for smoke evaluation."
            ),
            "public_demo_boundary": (
                "The ADK task agent does not execute arbitrary generated Python in "
                "the public demo. It works through whitelisted templates and tools."
            ),
        },
        "meta_agent": {
            "original_role": (
                "Read evaluation results and modify task-agent or meta-agent code to "
                "improve future generations."
            ),
            "adk_role": (
                "Diagnose study or smoke-run outcomes, explain failure modes, and "
                "propose process or prompt improvements for human review."
            ),
            "public_demo_boundary": (
                "The ADK meta agent does not directly edit files, run shell commands, "
                "or launch Docker in the public demo."
            ),
        },
        "coordinator": (
            "The root hyper_adk agent routes between study manifests, patch examples, "
            "safe smoke tools, and specialist agents to provide a bounded financial "
            "research workflow."
        ),
        "safety_summary": (
            "This preserves the HyperAgents task/meta architecture while avoiding "
            "public arbitrary-code execution and investment advice."
        ),
    }
