#!/usr/bin/env python
"""
thirdweb AI SDK - OpenAI Integration Example

This script demonstrates how to use the thirdweb AI SDK with OpenAI Assistants API.

Requirements:
- Python 3.9+
- thirdweb-ai package
- openai package
- thirdweb CLIENT_SECRET (set in .env or directly)
- OpenAI API key (for actual usage)

Usage:
python agent_example.py
"""

import os
from dotenv import load_dotenv
from thirdweb_ai import Insight
from thirdweb_ai.adapters.openai import get_agents_tools

# Load from .env file or set directly
load_dotenv()
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    print("Error: CLIENT_SECRET not found. Set it in .env or directly in this script.")
    exit(1)

def main():
    print("thirdweb AI SDK - OpenAI Integration Example")
    print("-" * 50)
    
    # Initialize Insight and get tools
    insight = Insight(CLIENT_SECRET)
    tools = insight.get_tools()
    print(f"Got {len(tools)} blockchain tools from thirdweb")
    
    # Convert to OpenAI format
    openai_tools = get_agents_tools(tools)
    print(f"Converted to {len(openai_tools)} OpenAI-compatible tools")
    
    # Print example tool details
    if openai_tools:
        first_tool = openai_tools[0]
        print(f"\nExample tool: {first_tool.name}")
        print(f"Description: {first_tool.description[:100]}...")
    
    # Show how to use with OpenAI Assistants API
    print("\nTo use with OpenAI Assistants API:")
    print("""
# Install the OpenAI Python SDK
# pip install openai

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="your_openai_api_key")

# Create an Assistant with the tools
assistant = client.beta.assistants.create(
    name="Blockchain Assistant",
    instructions="You are a helpful assistant that can access blockchain data.",
    model="gpt-4-turbo",
    tools=openai_tools
)

# Create a Thread
thread = client.beta.threads.create()

# Add a message to the Thread
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Show me Vitalik's ETH balance"
)

# Run the Assistant on the Thread
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Get the response
# Note: In a real application, you would need to poll for completion
messages = client.beta.threads.messages.list(thread_id=thread.id)
""")
    
    print("\nExample complete!")

if __name__ == "__main__":
    main() 