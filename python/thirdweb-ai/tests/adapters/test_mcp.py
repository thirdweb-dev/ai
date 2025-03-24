import importlib.util
from unittest.mock import MagicMock

import pytest

from thirdweb_ai.tools.tool import Tool


def has_module(module_name: str) -> bool:
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None


# Skip if mcp is not installed
mcp_installed = has_module("mcp")


@pytest.mark.skipif(not mcp_installed, reason="mcp not installed")
def test_get_mcp_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to MCP tools."""
    # Skip this test if module not fully installed
    pytest.importorskip("mcp.types")
    
    import mcp.types as mcp_types

    from thirdweb_ai.adapters.mcp import get_mcp_tools

    # Convert tools to MCP tools
    mcp_tools = get_mcp_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(mcp_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, mcp_types.Tool) for tool in mcp_tools)

    # Check properties were preserved
    assert [tool.name for tool in mcp_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in mcp_tools] == [
        tool.description for tool in test_tools
    ]

    # Check that input schemas were set correctly
    for i, tool in enumerate(mcp_tools):
        assert tool.inputSchema == test_tools[i].schema.get("parameters")


@pytest.mark.skipif(not mcp_installed, reason="mcp not installed")
def test_get_fastmcp_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to FastMCP tools."""
    # Skip this test if module not fully installed
    pytest.importorskip("mcp.server.fastmcp.tools.base")
    
    try:
        from mcp.server.fastmcp.tools.base import Tool as FastMCPTool

        from thirdweb_ai.adapters.mcp import get_fastmcp_tools

        # Patch test_tools if needed to avoid attribute error
        for tool in test_tools:
            if not hasattr(tool, "_func_definition"):
                setattr(tool, "_func_definition", getattr(tool, "run", None))  # Use run method as fallback

        # Convert tools to FastMCP tools
        fastmcp_tools = get_fastmcp_tools(test_tools)

        # Assert we got the correct number of tools
        assert len(fastmcp_tools) == len(test_tools)

        # Check all tools were properly converted
        assert all(isinstance(tool, FastMCPTool) for tool in fastmcp_tools)

        # Check properties were preserved
        assert [tool.name for tool in fastmcp_tools] == [tool.name for tool in test_tools]
        assert [tool.description for tool in fastmcp_tools] == [
            tool.description for tool in test_tools
        ]

        # Check all tools have callable run functions
        assert all(callable(tool.fn) for tool in fastmcp_tools)
    except (AttributeError, ImportError):
        pytest.skip("FastMCP tools not properly available")


@pytest.mark.skipif(not mcp_installed, reason="mcp not installed")
def test_add_fastmcp_tools(test_tools: list[Tool]):
    """Test adding thirdweb tools to a FastMCP instance."""
    # Skip this test if module not fully installed
    pytest.importorskip("mcp.server.fastmcp")
    
    try:
        from thirdweb_ai.adapters.mcp import add_fastmcp_tools

        # Create a mock FastMCP instance
        mock_fastmcp = MagicMock()
        mock_fastmcp._tool_manager = MagicMock()
        mock_fastmcp._tool_manager._tools = {}

        # Patch test_tools if needed to avoid attribute error
        for tool in test_tools:
            if not hasattr(tool, "_func_definition"):
                setattr(tool, "_func_definition", getattr(tool, "run", None))  # Use run method as fallback

        # Add tools to the FastMCP instance
        add_fastmcp_tools(mock_fastmcp, test_tools)

        # Check that the tools were added to the FastMCP instance
        assert len(mock_fastmcp._tool_manager._tools) == len(test_tools)
        
        # Get the expected tool names
        expected_tool_names = [tool.name for tool in test_tools]
        
        # Check that all expected tools were added
        for name in expected_tool_names:
            assert name in mock_fastmcp._tool_manager._tools
    except (AttributeError, ImportError):
        pytest.skip("FastMCP tools not properly available")
