import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if llama_index is not installed
llama_index_installed = has_module("llama_index")


@pytest.mark.skipif(not llama_index_installed, reason="llama-index not installed")
def test_get_llama_index_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to LlamaIndex tools."""
    from llama_index.core.tools import FunctionTool  # type: ignore[import]

    from thirdweb_ai.adapters.llama_index import get_llama_index_tools

    # Convert tools to LlamaIndex tools
    llama_tools = get_llama_index_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(llama_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, FunctionTool) for tool in llama_tools)

    # Check properties were preserved
    assert [tool.metadata.name for tool in llama_tools] == [tool.name for tool in test_tools]
    assert [tool.metadata.description for tool in llama_tools] == [tool.description for tool in test_tools]
    assert [tool.metadata.fn_schema for tool in llama_tools] == [tool.args_type() for tool in test_tools]

    # Check all tools are callable
    assert all(callable(tool) for tool in llama_tools)


@pytest.mark.skipif(not llama_index_installed, reason="llama-index-core not installed")
def test_get_llama_index_tools_return_direct(test_tools: list[Tool]):
    """Test LlamaIndex tools with return_direct=True."""
    from thirdweb_ai.adapters.llama_index import get_llama_index_tools

    # Convert tools to LlamaIndex tools with return_direct=True
    llama_tools = get_llama_index_tools(test_tools, return_direct=True)

    # Assert return_direct is set correctly
    assert all(tool.metadata.return_direct is True for tool in llama_tools)
