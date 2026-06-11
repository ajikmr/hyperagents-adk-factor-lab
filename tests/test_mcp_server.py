import pytest


def test_mcp_server_exposes_read_only_tools():
    pytest.importorskip("google.adk.tools.function_tool")
    pytest.importorskip("mcp")

    from hyper_adk.mcp_server import list_tool_names

    names = set(list_tool_names())
    assert "list_available_studies" in names
    assert "get_study_summary" in names
    assert "compare_conditions" in names
    assert "list_learning_patch_examples" in names
    assert "inspect_learning_patch" in names
    assert "explain_task_meta_roles" in names
    assert "list_smoke_datasets" in names
    assert "list_smoke_engine_runs" in names
    assert "inspect_smoke_engine_run" in names
    assert "finance_safety_check" in names

    assert "run_smoke_self_learning_cycle" not in names
    assert "run_smoke_cycle" not in names
    assert "docker" not in " ".join(names).lower()
