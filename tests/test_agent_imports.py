import pytest


def test_adk_agent_imports():
    pytest.importorskip("google.adk.agents")

    from hyper_adk.agent import MODEL, root_agent as main_agent
    from hyper_adk.sub_agents.meta_agent import meta_agent
    from hyper_adk.sub_agents.task_agent import task_agent
    from hyper_adk_mcp.agent import root_agent as mcp_agent
    from hyper_engine_adk.agent import root_agent as smoke_agent

    assert MODEL
    assert main_agent.name == "hyperagents_adk_factor_lab"
    assert task_agent.name == "hyper_task_agent"
    assert meta_agent.name == "hyper_meta_agent"
    assert smoke_agent.name == "hyperagents_smoke_cycle"
    assert mcp_agent.name == "hyperagents_adk_mcp_client"
