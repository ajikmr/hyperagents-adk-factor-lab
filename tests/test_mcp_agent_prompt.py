from hyper_adk_mcp.agent import MCP_CLIENT_PROMPT


def test_mcp_client_prompt_forbids_nonexistent_list_tools():
    assert "Do not call `mcp:list_tools`" in MCP_CLIENT_PROMPT
    assert "Do not call any tool whose name starts with `mcp:`" in MCP_CLIENT_PROMPT
    assert "list_available_studies" in MCP_CLIENT_PROMPT
    assert "If asked to list studies, call `list_available_studies` directly" in MCP_CLIENT_PROMPT
