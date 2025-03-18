import asyncio
import os

from llama_index.core.agent import FunctionCallingAgent
from llama_index.llms.openai import OpenAI
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.llama_index import get_llama_index_tools

# Initialize Thirdweb Insight and Nebula with API key
insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))


async def main():
    """Example of using thirdweb_ai with LlamaIndex."""

    # Create a LlamaIndex agent with thirdweb tools
    agent = FunctionCallingAgent.from_tools(
        tools=get_llama_index_tools(insight.get_tools() + nebula.get_tools()),
        llm=OpenAI(model="gpt-4o-mini"),
        max_function_calls=10,
        allow_parallel_tool_calls=False,
        verbose=True,
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

        result = agent.chat(query)

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
