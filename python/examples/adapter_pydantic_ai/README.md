# thirdweb-ai with Pydantic AI

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [Pydantic AI](https://github.com/pydantic/pydantic-ai), a framework for building AI systems with structured data.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with Pydantic AI to create an agent that can answer blockchain-related queries with the benefit of type safety and validation.

The example creates a Pydantic AI agent with thirdweb's blockchain tools, allowing you to interact with blockchain data through natural language while maintaining the structure and validation that Pydantic provides.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[pydantic_ai]"

# Using Poetry
poetry add "thirdweb-ai[pydantic_ai]"
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
- Query token data
- Access on-chain data through natural language

## Customization

You can customize the agent by modifying the example code:
- Change the model by modifying the model name in the `Agent` initialization
- Adjust the system prompt to set specific behavior guidelines
- Add custom queries to the `queries` list
- Configure specific blockchain networks by modifying the `chain_id` parameter

## Requirements

See `pyproject.toml` for the full list of dependencies. 