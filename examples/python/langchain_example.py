#!/usr/bin/env python
"""
thirdweb AI SDK - LangChain Integration Example

This script demonstrates how to use the thirdweb AI SDK with LangChain.

Requirements:
- Python 3.9+
- thirdweb-ai package
- langchain package
- thirdweb CLIENT_SECRET (set in .env or directly)
- OpenAI API key (for LangChain's ChatOpenAI)

Usage:
python langchain_example.py
"""

import os
from dotenv import load_dotenv
from thirdweb_ai import Insight
from thirdweb_ai.adapters.langchain import get_langchain_tools

# Load from .env file or set directly
load_dotenv()
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    print("Error: CLIENT_SECRET not found. Set it in .env or directly in this script.")
    exit(1)

def main():
    print("thirdweb AI SDK - LangChain Integration Example")
    print("-" * 50)
    
    # Initialize Insight and get tools
    insight = Insight(CLIENT_SECRET)
    tools = insight.get_tools()
    print(f"Got {len(tools)} blockchain tools from thirdweb")
    
    # Convert to LangChain format
    langchain_tools = get_langchain_tools(tools)
    print(f"Converted to {len(langchain_tools)} LangChain-compatible tools")
    
    # Print example tool details
    if langchain_tools:
        first_tool = langchain_tools[0]
        print(f"\nExample tool: {first_tool.name}")
        print(f"Description: {first_tool.description[:100]}...")
    
    # Show how to use with LangChain
    print("\nTo use with LangChain:")
    print("""
# Install required packages
# pip install langchain langchain-openai

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# Create a prompt
prompt = ChatPromptTemplate.from_template(
    "You are a blockchain assistant. Answer the following question: {input}"
)

# Create an agent with the tools
agent = create_tool_calling_agent(llm, langchain_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=langchain_tools)

# Execute the agent
result = agent_executor.invoke({"input": "What's the current ETH price?"})
print(result["output"])
""")
    
    print("\nExample complete!")

if __name__ == "__main__":
    main() 