import os
import sys

from coinbase_agentkit import (
    AgentKit,
    AgentKitConfig,
    EthAccountWalletProvider,
    EthAccountWalletProviderConfig,
)
from coinbase_agentkit_langchain import get_langchain_tools
from eth_account import Account
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.coinbase_agentkit import thirdweb_action_provider

# Initialize Thirdweb Insight and Nebula with API key
insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))


def initialize_agent():
    """Initialize the agent with Coinbase AgentKit."""

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Initialize wallet (use a test private key for this example)
    # WARNING: Never use this private key for actual funds, this is for testing only
    account = Account.create()

    # Initialize Ethereum Account Wallet Provider
    wallet_provider = EthAccountWalletProvider(
        config=EthAccountWalletProviderConfig(
            account=account,
            chain_id="8453",  # Base mainnet
            rpc_url="https://8453.rpc.thirdweb.com",
        )
    )

    # Initialize AgentKit with thirdweb tools
    agentkit = AgentKit(
        AgentKitConfig(
            wallet_provider=wallet_provider,
            action_providers=[
                thirdweb_action_provider(insight.get_tools() + nebula.get_tools()),
            ],
        )
    )

    # Get AgentKit tools for LangChain
    tools = get_langchain_tools(agentkit)

    # Store buffered conversation history in memory
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "thirdweb"}}

    # Create ReAct Agent using the LLM and AgentKit tools
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=(
            "You are a helpful blockchain assistant that can interact with the Ethereum blockchain. "
            "You have tools to query blockchain data and interact with smart contracts. "
            "Use the thirdweb actions to get information about ENS names and wallet balances."
        ),
    ), config


def run_agent_with_query(agent_executor, config, query):
    """Run the agent with a specific query."""
    print(f"\n\nQuery: {query}")
    print("-" * 50)

    # Store the agent's response chunks
    response_chunks = []

    # Run the agent
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=query)]}, config
    ):
        if "agent" in chunk:
            response = chunk["agent"]["messages"][0].content
            response_chunks.append(response)
            print(response)
        elif "tools" in chunk:
            tool_content = chunk["tools"]["messages"][0].content
            print(f"[Tool Output]: {tool_content}")
        print("-" * 30)

    # Return the full response
    return "".join(response_chunks)


def main():
    """Example of using thirdweb_ai with Coinbase AgentKit."""
    try:
        # Initialize the agent
        agent_executor, config = initialize_agent()

        # Example queries to demonstrate capabilities
        queries = [
            "What's the current balance of thirdweb.eth?",
            "When is the most recent transaction hash and timestamp of thirdweb.eth?",
        ]

        # Run queries
        for query in queries:
            run_agent_with_query(agent_executor, config, query)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
