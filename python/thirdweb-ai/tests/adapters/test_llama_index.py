import pytest

from thirdweb_ai.tools.tool import Tool


def test_get_llama_index_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to LlamaIndex tools."""
    pytest.importorskip("llama_index")
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
