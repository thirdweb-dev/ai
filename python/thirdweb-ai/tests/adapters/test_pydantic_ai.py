import pytest

from thirdweb_ai.tools.tool import Tool


def test_get_pydantic_ai_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to Pydantic AI tools."""
    pytest.importorskip("pydantic_ai")
    from pydantic_ai import Tool as PydanticTool  # type: ignore[import]

    from thirdweb_ai.adapters.pydantic_ai import get_pydantic_ai_tools

    # Convert tools to Pydantic AI tools
    pydantic_ai_tools = get_pydantic_ai_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(pydantic_ai_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, PydanticTool) for tool in pydantic_ai_tools)

    # Check properties were preserved
    assert [tool.name for tool in pydantic_ai_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in pydantic_ai_tools] == [tool.description for tool in test_tools]

    # Check all tools have function and prepare methods
    assert all(callable(getattr(tool, "function", None)) for tool in pydantic_ai_tools)
    assert all(callable(getattr(tool, "prepare", None)) for tool in pydantic_ai_tools)
