import asyncio
import os

from agents import Agent, Runner
from thirdweb_ai import Engine, Insight, Nebula
from thirdweb_ai.adapters.openai import get_agents_tools

# Initialize Thirdweb Insight and Nebula with API key
insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))
engine = Engine(
    engine_url=os.getenv("THIRDWEB_ENGINE_URL"),
    engine_auth_jwt=os.getenv("THIRDWEB_ENGINE_AUTH_JWT"),
    backend_wallet_address=os.getenv("THIRDWEB_BACKEND_WALLET_ADDRESS"),
)


async def main():
    """Example of using thirdweb_ai with OpenAI's agents framework."""

    # Create an agent with thirdweb tools
    agent = Agent(
        name="Blockchain Assistant",
        instructions="You are a helpful blockchain assistant. Use the provided tools to interact with the blockchain.",
        tools=get_agents_tools(
            insight.get_tools() + engine.get_tools() + nebula.get_tools()
        ),
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
