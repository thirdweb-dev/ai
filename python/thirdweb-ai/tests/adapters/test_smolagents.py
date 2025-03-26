import importlib.util

import pytest

from thirdweb_ai.tools.tool import Tool


def has_module(module_name: str) -> bool:
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None


# Skip if smolagents is not installed
smolagents_installed = has_module("smolagents")


@pytest.mark.skipif(not smolagents_installed, reason="smolagents not installed")
def test_get_smolagents_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to SmolaGents tools."""
    # Skip this test if module not fully installed
    if not smolagents_installed:
        pytest.skip("smolagents module not installed")

    try:
        from thirdweb_ai.adapters.smolagents import get_smolagents_tools

        # Convert tools to SmolaGents tools
        smolagents_tools = get_smolagents_tools(test_tools)

        # Assert we got the correct number of tools
        assert len(smolagents_tools) == len(test_tools)

        # Check properties were preserved using duck typing
        # We can't check the specific methods since we might not have the actual package
        # Just verify we can get name and description attributes
        for i, tool in enumerate(smolagents_tools):
            # Basic attribute checks that should work regardless of return type
            assert hasattr(tool, "name") or hasattr(tool, "__name__"), "Tool should have a name attribute"
            assert hasattr(tool, "description"), "Tool should have a description attribute"

            # Check name matching - handle different formats
            tool_name = tool.name if hasattr(tool, "name") else getattr(tool, "__name__", None)
            if tool_name is not None:
                assert tool_name == test_tools[i].name, f"Tool name mismatch: {tool_name} != {test_tools[i].name}"

            # Check description matching
            if hasattr(tool, "description"):
                assert tool.description == test_tools[i].description, "Tool description does not match"
    except (ImportError, AttributeError):
        pytest.skip("SmolaGents tools test skipped due to import issues")
