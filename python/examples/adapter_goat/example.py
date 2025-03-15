import os

from eth_account import Account
from eth_account.signers.local import LocalAccount
from goat_adapters.langchain import get_on_chain_tools
from goat_plugins.erc20 import ERC20PluginOptions, erc20
from goat_plugins.erc20.token import USDC
from goat_wallets.web3 import Web3EVMWalletClient
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.goat import ThirdwebPlugin
from web3 import Web3
from web3.middleware import SignAndSendRawMiddlewareBuilder


def main():
    """Example of using thirdweb_ai with GOAT SDK."""

    # Initialize Thirdweb Insight and Nebula with API key
    insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
    nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))

    # Initialize Web3 provider (using Base Sepolia testnet)
    w3 = Web3(Web3.HTTPProvider("https://84532.rpc.thirdweb.com"))

    # Initialize wallet (use a test private key for this example)
    # WARNING: Never use this private key for actual funds, this is for testing only
    account: LocalAccount = Account.create()

    # Set default account and add middleware for signing transactions
    w3.eth.default_account = account.address
    w3.middleware_onion.add(SignAndSendRawMiddlewareBuilder.build(account))

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful blockchain assistant. You can use thirdweb tools to interact with the blockchain.",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Initialize tools with GOAT wallet and plugins
    tools = get_on_chain_tools(
        wallet=Web3EVMWalletClient(w3),
        plugins=[
            # Add ERC20 token plugin for token interactions
            erc20(options=ERC20PluginOptions(tokens=[USDC])),
            # Add thirdweb plugin for blockchain queries
            ThirdwebPlugin(insight.get_tools() + nebula.get_tools()),
        ],
    )

    # Display available tools
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    print("\n")

    # Create agent with tools
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, handle_parsing_errors=True, verbose=True
    )

    # Example queries to demonstrate capabilities
    queries = [
        "What's the current balance of thirdweb.eth?",
        "When is the most recent transaction hash and timestamp of thirdweb.eth?",
    ]

    # Run the queries
    for query in queries:
        print(f"\n\nQuery: {query}")
        print("-" * 50)

        response = agent_executor.invoke(
            {
                "input": query,
            }
        )

        print("\nFinal Response:")
        print(response["output"])


if __name__ == "__main__":
    main()
