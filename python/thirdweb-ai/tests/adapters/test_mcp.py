import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool


def test_get_mcp_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to MCP tools."""
    pytest.importorskip("mcp.types")

    import mcp.types as mcp_types  # type: ignore[import]

    from thirdweb_ai.adapters.mcp import get_mcp_tools

    # Convert tools to MCP tools
    mcp_tools = get_mcp_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(mcp_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, mcp_types.Tool) for tool in mcp_tools)

    # Check properties were preserved
    assert [tool.name for tool in mcp_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in mcp_tools] == [tool.description for tool in test_tools]

    # Check that input schemas were set correctly
    for i, tool in enumerate(mcp_tools):
        assert tool.inputSchema == test_tools[i].schema.get("parameters")
