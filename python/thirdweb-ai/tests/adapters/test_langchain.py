import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if langchain-core is not installed
langchain_installed = has_module("langchain_core")


@pytest.mark.skipif(not langchain_installed, reason="langchain-core not installed")
def test_get_langchain_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to LangChain tools."""
    from langchain_core.tools.structured import StructuredTool  # type: ignore[import]

    from thirdweb_ai.adapters.langchain import get_langchain_tools

    # Convert tools to LangChain tools
    langchain_tools = get_langchain_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(langchain_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, StructuredTool) for tool in langchain_tools)

    # Check properties were preserved
    assert [tool.name for tool in langchain_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in langchain_tools] == [tool.description for tool in test_tools]

    # Check schemas were preserved
    assert [tool.args_schema for tool in langchain_tools] == [tool.args_type() for tool in test_tools]

    # Check all tools have callable run methods
    assert all(callable(getattr(tool, "func", None)) for tool in langchain_tools)
