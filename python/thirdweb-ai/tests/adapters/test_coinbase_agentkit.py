import importlib.util

import pytest

from thirdweb_ai.tools.tool import Tool


def has_module(module_name: str) -> bool:
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None


# Skip if coinbase_agentkit is not installed
coinbase_agentkit_installed = has_module("coinbase_agentkit")


@pytest.mark.skipif(not coinbase_agentkit_installed, reason="coinbase-agentkit not installed")
def test_get_coinbase_agentkit_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to Coinbase AgentKit tools."""
    # Import needed here to avoid import errors if module is not installed
    from coinbase_agentkit.action_providers.action_decorator import ActionMetadata

    from thirdweb_ai.adapters.coinbase_agentkit import thirdweb_action_provider

    # Convert tools to Coinbase AgentKit tools
    provider = thirdweb_action_provider(test_tools)

    # Check provider was created
    assert provider is not None
    assert provider.name == "thirdweb"

    # Check provider has actions
    assert len(provider._actions) == len(test_tools)
    
    # Check all actions are properly set up
    assert all(isinstance(action, ActionMetadata) for action in provider._actions)

    # Check properties were preserved
    assert [action.name for action in provider._actions] == [tool.name for tool in test_tools]
    assert [action.description for action in provider._actions] == [
        tool.description for tool in test_tools
    ]

    # Verify that args_schema is set correctly
    assert [action.args_schema for action in provider._actions] == [
        tool.args_type() for tool in test_tools
    ]
    
    # Check all actions have callable invoke functions
    assert all(callable(action.invoke) for action in provider._actions)