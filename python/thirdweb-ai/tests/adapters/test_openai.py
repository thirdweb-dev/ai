import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if openai is not installed
openai_installed = has_module("openai")


@pytest.mark.skipif(not openai_installed, reason="openai not installed")
def test_get_openai_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to OpenAI tools."""
    pytest.importorskip("openai")

    from thirdweb_ai.adapters.openai import get_openai_tools

    # Convert tools to OpenAI tools
    openai_tools = get_openai_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(openai_tools) == len(test_tools)

    # Check all required properties exist in the tools
    for i, tool in enumerate(openai_tools):
        assert isinstance(tool, dict)
        assert "type" in tool
        assert "function" in tool
        assert "name" in tool["function"]
        assert "description" in tool["function"]
        assert "parameters" in tool["function"]

        # Check name and description match
        assert tool["function"]["name"] == test_tools[i].name
        assert tool["function"]["description"] == test_tools[i].description
