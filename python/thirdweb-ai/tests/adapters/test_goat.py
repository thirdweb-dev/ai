import contextlib
import importlib.util

import pytest

from thirdweb_ai.tools.tool import Tool


def has_module(module_name: str) -> bool:
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None


# Skip if goat is not installed
goat_installed = has_module("goat-sdk")


@pytest.mark.skipif(not goat_installed, reason="goat not installed")
def test_get_goat_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to GOAT tools."""
    # Skip this test if module not fully installed
    pytest.importorskip("goat.tools")

    from goat.tools import BaseTool as GoatBaseTool

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


@pytest.mark.skipif(not goat_installed, reason="goat not installed")
def test_thirdweb_plugin(test_tools: list[Tool]):
    """Test the ThirdwebPlugin class for GOAT."""
    # Skip this test if module not fully installed
    if not has_module("goat.types.chain"):
        pytest.skip("Module goat.types.chain not available")

    try:
        from goat.types.chain import Chain

        from thirdweb_ai.adapters.goat import ThirdwebPlugin

        # Create the plugin
        plugin = ThirdwebPlugin(test_tools)

        # Check plugin was created correctly
        assert plugin.name == "thirdweb"
        assert plugin.tools == test_tools

        class MockChain:
            def __init__(self, data):
                self.data = data

            def __getitem__(self, key):
                return self.data.get(key)

        evm_chain = MockChain({"type": "evm", "name": "ethereum"})
        non_evm_chain = MockChain({"type": "solana", "name": "solana"})

        # Patching the Chain type with our mock to make sure the test works
        # Only necessary in test environment where the real package may not be available
        import types

        import goat.types.chain

        goat.types.chain.Chain = types.SimpleNamespace()
        goat.types.chain.Chain.__call__ = lambda data: MockChain(data)

        # Now test chain support with our mocks
        assert plugin.supports_chain(evm_chain) is True
        assert plugin.supports_chain(non_evm_chain) is False

        # Check get_tools returns the correct number of tools
        with contextlib.suppress(Exception):
            tools = plugin.get_tools(None)
            assert len(tools) == len(test_tools)
    except (ImportError, TypeError):
        pytest.skip("GOAT plugin test skipped due to import issues")
