from coinbase_agentkit import ActionProvider, EvmWalletProvider
from coinbase_agentkit.action_providers.action_decorator import ActionMetadata
from coinbase_agentkit.network import Network
from thirdweb_ai import Tool


class ThirdwebActionProvider(ActionProvider[EvmWalletProvider]):
    """Action provider for Thirdweb."""

    def __init__(self, tools: list[Tool]) -> None:
        """Initialize the Thirdweb action provider."""
        super().__init__("thirdweb", [])
        self._actions = []
        for tool in tools:
            self.register_action(tool)

    def register_action(self, tool: Tool) -> None:
        self._actions.append(
            ActionMetadata(
                name=tool.name,
                description=tool.description,
                args_schema=tool.args_type(),
                invoke=lambda provider, args: tool.run_json(args),
                wallet_provider=False,
            )
        )

    def supports_network(self, network: Network) -> bool:
        return network.protocol_family == "evm"


def thirdweb_action_provider(tools: list[Tool]) -> ThirdwebActionProvider:
    return ThirdwebActionProvider(tools)
