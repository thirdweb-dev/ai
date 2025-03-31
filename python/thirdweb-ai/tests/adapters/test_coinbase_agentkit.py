import pytest

from thirdweb_ai.common.utils import has_module
from thirdweb_ai.tools.tool import Tool

# Skip if coinbase_agentkit is not installed
coinbase_agentkit_installed = has_module("coinbase_agentkit")


@pytest.mark.skipif(not coinbase_agentkit_installed, reason="coinbase-agentkit not installed")
def test_get_coinbase_agentkit_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to Coinbase AgentKit tools."""
    # Import needed here to avoid import errors if module is not installed
    from coinbase_agentkit import ActionProvider  # type: ignore[import]

    from thirdweb_ai.adapters.coinbase_agentkit import ThirdwebActionProvider, thirdweb_action_provider

    # Convert tools to Coinbase AgentKit provider
    provider = thirdweb_action_provider(test_tools)

    # Check provider was created with the right type
    assert isinstance(provider, ThirdwebActionProvider)
    assert isinstance(provider, ActionProvider)

    # Check provider name
    assert provider.name == "thirdweb"

    # Check provider has the expected number of actions
    assert len(provider.get_actions()) == len(test_tools)

    # Check properties were preserved by getting actions and checking names/descriptions
    actions = provider.get_actions()
    assert [action.name for action in actions] == [tool.name for tool in test_tools]
    assert [action.description for action in actions] == [tool.description for tool in test_tools]

    # Verify that args_schema is set correctly
    assert [action.args_schema for action in actions] == [tool.args_type() for tool in test_tools]

    # Check all actions have callable invoke functions
    assert all(callable(action.invoke) for action in actions)
