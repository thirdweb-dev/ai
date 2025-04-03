import pytest
from coinbase_agentkit import (
    EthAccountWalletProvider,
    EthAccountWalletProviderConfig,
)
from eth_account import Account

from thirdweb_ai.tools.tool import Tool


def test_get_coinbase_agentkit_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to Coinbase AgentKit tools."""
    pytest.importorskip("coinbase_agentkit")
    from coinbase_agentkit import ActionProvider  # type: ignore[import]

    from thirdweb_ai.adapters.coinbase_agentkit import ThirdwebActionProvider, thirdweb_action_provider

    # Convert tools to Coinbase AgentKit provider
    provider = thirdweb_action_provider(test_tools)

    # Check provider was created with the right type
    assert isinstance(provider, ThirdwebActionProvider)
    assert isinstance(provider, ActionProvider)

    # Check provider name
    assert provider.name == "thirdweb"

    account = Account.create()
    # Initialize Ethereum Account Wallet Provider
    wallet_provider = EthAccountWalletProvider(
        config=EthAccountWalletProviderConfig(
            account=account,
            chain_id="8453",  # Base mainnet
            rpc_url="https://8453.rpc.thirdweb.com",
        )
    )
    actions = provider.get_actions(wallet_provider=wallet_provider)
    # Check provider has the expected number of actions
    assert len(actions) == len(test_tools)

    # Check properties were preserved by getting actions and checking names/descriptions
    assert [action.name for action in actions] == [tool.name for tool in test_tools]
    assert [action.description for action in actions] == [tool.description for tool in test_tools]

    # Verify that args_schema is set correctly
    assert [action.args_schema for action in actions] == [tool.args_type() for tool in test_tools]

    # Check all actions have callable invoke functions
    assert all(callable(action.invoke) for action in actions)
