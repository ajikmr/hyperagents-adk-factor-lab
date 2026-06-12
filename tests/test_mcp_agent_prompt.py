from hyper_adk_mcp.agent import MCP_CLIENT_PROMPT


def test_mcp_client_prompt_forbids_nonexistent_list_tools():
    assert "Do not call `mcp:list_tools`" in MCP_CLIENT_PROMPT
    assert "Do not call any tool whose name starts with `mcp:`" in MCP_CLIENT_PROMPT
    assert "list_available_studies" in MCP_CLIENT_PROMPT
    assert "mcp_fallback_list_available_studies" in MCP_CLIENT_PROMPT


def test_mcp_client_agent_has_fallback_tools():
    from hyper_adk_mcp.agent import root_agent

    tool_names = {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in root_agent.tools}
    assert "mcp_fallback_list_available_studies" in tool_names
    assert "mcp_fallback_explain_task_meta_roles" in tool_names
