import os

from smolagents import OpenAIServerModel, ToolCallingAgent
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.smolagents import get_smolagents_tools


def main():
    """Example of using thirdweb_ai with SmolAgents."""

    # Initialize Thirdweb Insight and Nebula with API key
    insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
    nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))

    # Initialize the OpenAI model
    model = OpenAIServerModel(model_id="gpt-4o-mini")

    # Get thirdweb tools for SmolAgents
    tools = get_smolagents_tools(insight.get_tools() + nebula.get_tools())

    # Create an agent with the tools
    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        max_steps=3,  # Limit to 3 steps to prevent infinite loops
    )

    # Print available tools
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    print("\n")

    # Example queries to demonstrate capabilities
    queries = [
        "What's the current balance of thirdweb.eth?",
        "When is the most recent transaction hash and timestamp of thirdweb.eth?",
    ]

    # Run the queries
    for query in queries:
        print(f"\n\nQuery: {query}")
        print("-" * 50)

        result = agent.run(query)

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    main()
