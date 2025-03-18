import os

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.langchain import get_langchain_tools


def main():
    """Example of using thirdweb_ai with LangChain."""

    # Initialize Thirdweb Insight and Nebula with API key
    insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
    nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful blockchain assistant. You can use the thirdweb tools to interact with the blockchain.",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Get thirdweb tools for LangChain
    tools = get_langchain_tools(insight.get_tools() + nebula.get_tools())

    # Display available tools
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    print("\n")

    # Create the agent
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
