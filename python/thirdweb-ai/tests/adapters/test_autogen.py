import importlib.util

import pytest

from thirdweb_ai.tools.tool import Tool


def has_module(module_name: str) -> bool:
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None


# Skip if autogen-core is not installed
autogen_installed = has_module("autogen_core")


@pytest.mark.skipif(not autogen_installed, reason="autogen-core not installed")
def test_get_autogen_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to AutoGen tools."""
    from autogen_core.tools import BaseTool as AutogenBaseTool

    from thirdweb_ai.adapters.autogen import get_autogen_tools

    # Convert tools to AutoGen tools
    autogen_tools = get_autogen_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(autogen_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, AutogenBaseTool) for tool in autogen_tools)

    # Check properties were preserved
    assert [tool.name for tool in autogen_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in autogen_tools] == [tool.description for tool in test_tools]

    # Check all tools have a run method
    assert all(callable(getattr(tool, "run", None)) for tool in autogen_tools)


@pytest.mark.skipif(not autogen_installed, reason="autogen-core not installed")
def test_autogen_tool_underlying_tool(test_tool: Tool):
    """Test that the wrapped tool can access the original thirdweb tool."""
    from thirdweb_ai.adapters.autogen import get_autogen_tools

    # Convert a single tool
    autogen_tools = get_autogen_tools([test_tool])

    # Check we got one tool
    assert len(autogen_tools) == 1

    # Get the wrapped tool
    wrapped_tool = autogen_tools[0]

    # Check it has access to the original tool
    assert hasattr(wrapped_tool, "tool")
    assert wrapped_tool.tool == test_tool
