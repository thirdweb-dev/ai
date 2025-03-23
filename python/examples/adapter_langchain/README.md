# thirdweb-ai with LangChain

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [LangChain](https://github.com/langchain-ai/langchain), a popular framework for building applications with large language models.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with LangChain to create an agent that can answer queries about blockchain data, resolve ENS names, check wallet balances, and access on-chain information through natural language.

The example creates a LangChain agent with thirdweb's tools and demonstrates how to query blockchain data using the tool-calling functionality to interact with Ethereum and other EVM chains.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[langchain]"

# Using uv
uv add "thirdweb-ai[langchain]"
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

The script demonstrates using the agent to:
- Check wallet balances
- Get transaction information
- Resolve ENS names
- Query token metadata
- And more!

## Customization

You can customize the agent by modifying the example code:
- Change the system prompt to specialize the agent behavior
- Add different chain IDs to query other blockchains
- Modify the queries to suit your specific use cases

## Requirements

See `pyproject.toml` for the full list of dependencies. 
