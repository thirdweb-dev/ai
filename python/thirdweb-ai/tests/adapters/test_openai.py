import pytest

from thirdweb_ai.tools.tool import Tool


def test_get_openai_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to OpenAI tools."""
    pytest.importorskip("openai")
    from agents import FunctionTool

    from thirdweb_ai.adapters.openai import get_openai_tools

    # Convert tools to OpenAI tools
    openai_tools = get_openai_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(openai_tools) == len(test_tools)

    # Check all required properties exist in the tools
    for i, tool in enumerate(openai_tools):
        assert isinstance(tool, FunctionTool)
        assert hasattr(tool, "name")
        assert hasattr(tool, "description")
        assert hasattr(tool, "params_json_schema")

        # Check name and description match
        assert tool.name == test_tools[i].name
        assert tool.description == test_tools[i].description
