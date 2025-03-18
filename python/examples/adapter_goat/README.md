# thirdweb-ai with GOAT SDK

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with the [GOAT SDK](https://github.com/goat-sdk/goat), a framework for building on-chain agents.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to combine GOAT SDK's on-chain action capabilities with thirdweb's blockchain tools to create a powerful agent that can both query blockchain data and perform on-chain actions.

The example creates a LangChain agent with GOAT SDK wallet functionality and thirdweb's tools as a plugin, allowing you to query blockchain data (ENS resolution, balances, etc.) while also having the ability to interact with ERC20 tokens and other on-chain assets.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[goat]"

# Using Poetry
poetry add "thirdweb-ai[goat]"
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
- Interact with ERC20 tokens
- Access on-chain data through natural language

## Customization

You can customize the agent by modifying the example code:
- Use a different wallet implementation
- Add other GOAT SDK plugins
- Change the RPC endpoint to connect to different networks
- Adjust the system prompt to change agent behavior
- Add more complex queries involving token interactions

## Requirements

See `pyproject.toml` for the full list of dependencies. 