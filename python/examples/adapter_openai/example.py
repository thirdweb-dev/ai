import asyncio
import os

from agents import Agent, Runner
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.openai import get_agents_tools

# Initialize Thirdweb Insight and Nebula with API key
insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))


async def main():
    """Example of using thirdweb_ai with OpenAI's agents framework."""

    # Create an agent with thirdweb tools
    agent = Agent(
        name="Blockchain Assistant",
        instructions="You are a helpful blockchain assistant. Use the provided tools to interact with the blockchain.",
        tools=get_agents_tools(insight.get_tools() + nebula.get_tools()),
    )

    # Example queries to demonstrate capabilities
    queries = [
        "What's the current balance of thirdweb.eth?",
        "When is the most recent transaction hash and timestamp of thirdweb.eth?",
    ]

    for query in queries:
        print(f"\n\nQuery: {query}")
        print("-" * 50)

        # Execute the query
        result = await Runner.run(agent, query)

        # Print the result
        print("Response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
