import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.autogen import get_autogen_tools

# Initialize Thirdweb Insight and Nebula with API key
insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))


async def main():
    """Example of using thirdweb_ai with AutoGen."""

    # Create thirdweb tools for AutoGen
    tools = get_autogen_tools(insight.get_tools() + nebula.get_tools())

    # Create a cancellation token for the agent
    cancellation_token = CancellationToken()

    # Initialize the OpenAI model client
    model = OpenAIChatCompletionClient(model="gpt-4o-mini")

    # Create an assistant agent with thirdweb tools
    agent = AssistantAgent(
        "Assistant",
        model_client=model,
        tools=tools,
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

        result = await agent.run(
            task=query,
            cancellation_token=cancellation_token,
        )

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
