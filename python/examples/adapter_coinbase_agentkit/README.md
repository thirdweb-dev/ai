# thirdweb-ai with Coinbase AgentKit

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [Coinbase AgentKit](https://github.com/coinbase/agentkit), a framework for building on-chain agents.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to integrate these tools with Coinbase AgentKit to create an agent capable of both querying blockchain data and performing on-chain actions.

The example creates a LangGraph agent with Coinbase AgentKit and thirdweb's blockchain tools, allowing you to query on-chain data, resolve ENS names, check balances, and perform wallet operations through a unified interface.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[coinbase_agentkit]"

# Using Poetry
poetry add "thirdweb-ai[coinbase_agentkit]"
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
- Use wallet capabilities from AgentKit
- Access on-chain data through natural language

## Customization

You can customize the agent by modifying the example code:
- Use different wallet providers from AgentKit
- Change the chain configuration
- Add additional action providers
- Modify the state modifier to adjust agent behavior
- Customize the queries to explore different blockchain interactions

## Requirements

See `pyproject.toml` for the full list of dependencies. 