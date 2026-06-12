from hyper_adk_mcp.fallback_tools import (
    mcp_fallback_explain_task_meta_roles,
    mcp_fallback_list_available_studies,
)


def test_mcp_fallback_list_available_studies():
    result = mcp_fallback_list_available_studies()

    assert result["count"] == 4
    assert {study["id"] for study in result["studies"]} >= {
        "sp500_default_validation",
        "csi300_default_validation",
    }


def test_mcp_fallback_explain_task_meta_roles():
    result = mcp_fallback_explain_task_meta_roles()

    assert "task_agent" in result
    assert "meta_agent" in result
    assert "public demo" in result["meta_agent"]["public_demo_boundary"]
