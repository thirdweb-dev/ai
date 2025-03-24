# thirdweb-ai with OpenAI's Agents Framework

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with OpenAI's [Agents](https://github.com/openai/openai-agents-python), allowing you to create blockchain-capable AI assistants.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with OpenAI's Agents to create an AI assistant that can interact with blockchain data through natural language.

The example creates an agent using the OpenAI Agents framework combined with thirdweb's blockchain tools, enabling you to query on-chain data, resolve ENS names, check balances, and more.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[openai]"

# Using uv
uv add "thirdweb-ai[openai]"
```

## Usage

1. Set your thirdweb API key as an environment variable:
```bash
export THIRDWEB_SECRET_KEY=your_api_key_here
```

2. Run the example:
```bash
python example.py
```

The script demonstrates using the assistant to:
- Check wallet balances
- Get transaction information
- Resolve ENS names
- Query on-chain data
- And more!

## Customization

You can customize the assistant by modifying the example code:
- Change the agent name and instructions
- Add different types of queries to the `queries` list
- Adjust the chain ID to query different blockchains
- Configure additional tools as needed

## Requirements

See `pyproject.toml` for the full list of dependencies. 
