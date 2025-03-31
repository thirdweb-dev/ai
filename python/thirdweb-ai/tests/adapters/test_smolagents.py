import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if smolagents is not installed
smolagents_installed = has_module("smolagents")


@pytest.mark.skipif(not smolagents_installed, reason="smolagents not installed")
def test_get_smolagents_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to SmolaGents tools."""
    # Skip this test if module not fully installed
    pytest.importorskip("smolagents")

    from smolagents import Tool as SmolagentTool  # type: ignore[import]

    from thirdweb_ai.adapters.smolagents import get_smolagents_tools

    # Convert tools to SmolaGents tools
    smolagents_tools = get_smolagents_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(smolagents_tools) == len(test_tools)

    # Check all tools were properly converted (using duck typing with SmolagentTool)
    assert all(isinstance(tool, SmolagentTool) for tool in smolagents_tools)

    # Check properties were preserved
    assert [tool.name for tool in smolagents_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in smolagents_tools] == [tool.description for tool in test_tools]

    # Check all tools have a callable forward method
    assert all(callable(getattr(tool, "forward", None)) for tool in smolagents_tools)
