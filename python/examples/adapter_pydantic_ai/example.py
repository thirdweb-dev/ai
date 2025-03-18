import asyncio
import os

from pydantic_ai import Agent
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.pydantic_ai import get_pydantic_ai_tools

# Initialize Thirdweb Insight and Nebula with API key
insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))


async def main():
    """Example of using thirdweb_ai with Pydantic AI."""

    # Create a Pydantic AI agent with thirdweb tools
    tools = get_pydantic_ai_tools(insight.get_tools() + nebula.get_tools())
    agent = Agent(
        "openai:gpt-4o-mini",  # Use the OpenAI GPT-4o-mini model
        tools=tools,
        system_prompt=(
            "What's the current balance of thirdweb.eth?",
            "When is the most recent transaction hash and timestamp of thirdweb.eth?",
        ),
    )

    # Print available tools
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}")
    print("\n")

    # Example queries to demonstrate capabilities
    queries = [
        "What are the addresses associated to thirdweb.eth?",
        "What's the current balance of thirdweb.eth?",
    ]

    # Run the queries
    for query in queries:
        print(f"\n\nQuery: {query}")
        print("-" * 50)

        result = await agent.run(query)

        print("\nResult:")
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())
