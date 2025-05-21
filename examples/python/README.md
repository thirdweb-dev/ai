# thirdweb AI Python Examples

This directory contains Python examples for the thirdweb AI SDK.

## Examples

- **simple_demo.py**: A basic demo script that shows how to initialize the SDK, get tools, and prepare them for use with different AI frameworks.

- **agent_example.py**: Demonstrates how to integrate the thirdweb AI SDK with OpenAI Assistants API.

- **langchain_example.py**: Shows how to use the thirdweb AI SDK with LangChain for building AI agents with blockchain capabilities.

- **thirdweb_ai_summary.py**: A comprehensive overview of the SDK's capabilities, structure, and usage patterns.

## Running the Examples

These examples require:

1. Python 3.9+
2. thirdweb-ai package: `pip install "thirdweb-ai[all]"`
3. A thirdweb CLIENT_SECRET (set in a .env file or directly in the script)

Create a `.env` file in the same directory as the example scripts with your secret:

```
CLIENT_SECRET=your_thirdweb_client_secret_here
```

Then run any example:

```bash
python simple_demo.py
```

## Additional Requirements

- For OpenAI examples: `pip install openai`
- For LangChain examples: `pip install langchain langchain-openai`

## Key Concepts

The thirdweb AI SDK is primarily designed as a toolkit for AI agents to interact with blockchains. The basic usage pattern is:

1. Initialize a service (Insight, Nebula, Engine)
2. Get tools from the service
3. Convert tools to your AI framework format
4. Create an AI agent with these tools
5. Let the agent interact with blockchain data
