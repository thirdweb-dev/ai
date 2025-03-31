import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if goat is not installed
goat_installed = has_module("goat-sdk")


@pytest.mark.skipif(not goat_installed, reason="goat not installed")
def test_get_goat_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to GOAT tools."""
    # Skip this test if module not fully installed
    pytest.importorskip("goat.tools")

    from goat.tools import BaseTool as GoatBaseTool  # type: ignore[import]

    from thirdweb_ai.adapters.goat import get_goat_tools

    # Convert tools to GOAT tools
    goat_tools = get_goat_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(goat_tools) == len(test_tools)

    # Check all tools were properly converted
    assert all(isinstance(tool, GoatBaseTool) for tool in goat_tools)

    # Check properties were preserved
    assert [tool.name for tool in goat_tools] == [tool.name for tool in test_tools]
    assert [tool.description for tool in goat_tools] == [tool.description for tool in test_tools]

    # Check all tools have a callable run method
    assert all(callable(getattr(tool, "run", None)) for tool in goat_tools)
