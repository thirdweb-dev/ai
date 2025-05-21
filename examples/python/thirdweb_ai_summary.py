"""
thirdweb AI SDK Usage Summary

This script demonstrates how thirdweb-ai is intended to be used, based on our exploration.
"""

import os
from dotenv import load_dotenv
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.openai import get_agents_tools
from thirdweb_ai.adapters.langchain import get_langchain_tools

# Load environment variables
load_dotenv()
client_secret = os.getenv("CLIENT_SECRET")

print("=" * 50)
print("thirdweb AI SDK Usage Summary")
print("=" * 50)

# 1. Initialization
print("\n1. Initialization")
print("-" * 30)
print("The SDK provides three main services:")
print("- Insight: For blockchain data intelligence")
print("- Engine: For wallet management and transactions")
print("- Nebula: For AI agent blockchain interaction")
print("\nInitializing with CLIENT_SECRET:")
insight = Insight(client_secret)
try:
    nebula = Nebula(client_secret)
    print("✓ Both Insight and Nebula initialized successfully")
except Exception as e:
    print(f"✓ Insight initialized successfully")
    print(f"✗ Nebula initialization failed: {e}")

# 2. Tools
print("\n2. Tools")
print("-" * 30)
print("The SDK provides tools for AI agents to interact with blockchains:")
tools = insight.get_tools()
print(f"Number of tools from Insight: {len(tools)}")
print("\nAvailable tools:")
for i, tool in enumerate(tools, 1):
    print(f"{i}. {tool.name}: {tool.description[:60]}..." if len(tool.description) > 60 else f"{i}. {tool.name}: {tool.description}")

# 3. Framework Adapters
print("\n3. Framework Adapters")
print("-" * 30)
print("The SDK provides adapters for different AI frameworks:")

# OpenAI
try:
    openai_tools = get_agents_tools(tools)
    print(f"✓ OpenAI: Converted {len(openai_tools)} tools")
except Exception as e:
    print(f"✗ OpenAI adapter error: {e}")

# LangChain
try:
    langchain_tools = get_langchain_tools(tools)
    print(f"✓ LangChain: Converted {len(langchain_tools)} tools")
except Exception as e:
    print(f"✗ LangChain adapter error: {e}")

# 4. Usage Pattern
print("\n4. Usage Pattern")
print("-" * 30)
print("The intended usage pattern is:")
print("1. Initialize the thirdweb-ai services")
print("2. Get tools from the services")
print("3. Convert tools to your AI framework format (OpenAI, LangChain, etc.)")
print("4. Create an AI agent with these tools")
print("5. Let the agent use these tools to interact with blockchain data")

# 5. Example Usage (Pseudo-code)
print("\n5. Example Usage (Pseudo-code)")
print("-" * 30)
print("""
# OpenAI Example
from openai import OpenAI

client = OpenAI(api_key="your_openai_api_key")
assistant = client.beta.assistants.create(
    name="Blockchain Assistant",
    instructions="You are a helpful assistant that can access blockchain data.",
    model="gpt-4-turbo",
    tools=openai_tools
)

# LangChain Example
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("{input}")
agent = create_tool_calling_agent(llm, langchain_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=langchain_tools)
result = agent_executor.invoke({"input": "Show me Vitalik's ETH balance"})
""")

print("\n" + "=" * 50)
print("End of Summary")
print("=" * 50) 