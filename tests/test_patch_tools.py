import json
from pathlib import Path

from hyper_adk.tools import (
    explain_task_meta_roles,
    inspect_learning_patch,
    list_learning_patch_examples,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PATCH_EXAMPLES_PATH = PROJECT_ROOT / "hyper_adk" / "data" / "learning_patch_examples.json"


def test_learning_patch_examples_manifest_is_sanitized():
    payload = json.loads(PATCH_EXAMPLES_PATH.read_text(encoding="utf-8"))
    serialized = json.dumps(payload)

    assert len(payload["examples"]) == 2
    assert "__pycache__" not in serialized
    assert "Binary files" not in serialized
    assert "credentials" in serialized


def test_list_learning_patch_examples():
    result = list_learning_patch_examples()

    assert result["count"] == 2
    assert result["global_caveats"]
    assert {example["dataset"] for example in result["examples"]} == {
        "sp500",
        "csi300",
    }


def test_list_learning_patch_examples_filter():
    result = list_learning_patch_examples(dataset="sp500", agent_modified="task_agent")

    assert result["count"] == 1
    assert result["examples"][0]["id"] == "sp500_task_agent_robust_prompt_and_fallback"


def test_inspect_learning_patch():
    result = inspect_learning_patch("csi300_task_agent_factor_template_guidance")

    assert result["dataset"] == "csi300"
    assert result["agent_modified"] == "task_agent"
    assert result["sanitized_patch_excerpt"]
    assert "sanitization_note" in result
    assert "No stock recommendations" in " ".join(result["safety_caveats"])


def test_explain_task_meta_roles():
    result = explain_task_meta_roles()

    assert "task_agent" in result
    assert "meta_agent" in result
    assert "public demo" in result["task_agent"]["public_demo_boundary"]
    assert "Docker" in result["meta_agent"]["public_demo_boundary"]
