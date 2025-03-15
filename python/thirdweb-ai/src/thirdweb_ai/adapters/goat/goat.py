from goat import PluginBase, WalletClientBase, create_tool
from goat.types.chain import Chain
from thirdweb_ai import Tool


def get_goat_tools(tools: list[Tool]) -> list[create_tool]:
    return [
        create_tool(
            config={
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.args_type(),
            },
            execute_fn=lambda args, t=tool: t.run_json(args),
        )
        for tool in tools
    ]


class ThirdwebPlugin(PluginBase[WalletClientBase]):
    def __init__(self, tools: list[Tool]):
        super().__init__("thirdweb", [])
        self.tools = tools

    def supports_chain(self, chain: Chain) -> bool:
        return chain["type"] == "evm"

    def get_tools(self, wallet_client: WalletClientBase):
        return get_goat_tools(self.tools)
