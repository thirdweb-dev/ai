#!/usr/bin/env python
"""
thirdweb AI SDK Simple Demo

This script demonstrates basic usage of the thirdweb AI SDK and validates
that the installation is working correctly.

Requirements:
- Python 3.9+
- thirdweb-ai package
- thirdweb CLIENT_SECRET (set in .env or directly)

Usage:
python simple_demo.py
"""

import os
from dotenv import load_dotenv
from thirdweb_ai import Insight, Nebula

# Load from .env file or set directly
load_dotenv()
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    print("Error: CLIENT_SECRET not found. Set it in .env or directly in this script.")
    exit(1)

def main():
    print("thirdweb AI SDK Demo")
    print("-" * 30)
    
    # 1. Initialize Insight
    print("\n1. Initializing Insight service...")
    insight = Insight(CLIENT_SECRET)
    print("✓ Insight service initialized")
    
    # 2. Get tools
    print("\n2. Getting blockchain tools...")
    tools = insight.get_tools()
    print(f"✓ Got {len(tools)} tools")
    
    # 3. List available tools
    print("\n3. Available blockchain tools:")
    for i, tool in enumerate(tools, 1):
        print(f"   {i}. {tool.name}")
    
    # 4. Framework adapters
    print("\n4. Testing framework adapters...")
    
    # OpenAI adapter
    try:
        from thirdweb_ai.adapters.openai import get_agents_tools
        openai_tools = get_agents_tools(tools)
        print(f"✓ OpenAI adapter: {len(openai_tools)} tools")
    except Exception as e:
        print(f"✗ OpenAI adapter error: {str(e)[:60]}...")
    
    # LangChain adapter
    try:
        from thirdweb_ai.adapters.langchain import get_langchain_tools
        langchain_tools = get_langchain_tools(tools)
        print(f"✓ LangChain adapter: {len(langchain_tools)} tools")
    except Exception as e:
        print(f"✗ LangChain adapter error: {str(e)[:60]}...")
    
    # 5. Summary
    print("\nHow to use with AI frameworks:")
    print("1. Initialize service and get tools")
    print("2. Convert tools to your framework's format")
    print("3. Create an AI agent with the tools")
    print("4. Let the agent interact with blockchain data")
    
    print("\nDemo complete!")

if __name__ == "__main__":
    main() 