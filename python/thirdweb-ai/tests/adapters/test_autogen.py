import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if autogen-core is not installed
autogen_installed = has_module("autogen_core")


@pytest.mark.skipif(not autogen_installed, reason="autogen-core not installed")
def test_get_autogen_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to AutoGen tools."""
    from autogen_core.tools import BaseTool as AutogenBaseTool  # type: ignore[import]

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
