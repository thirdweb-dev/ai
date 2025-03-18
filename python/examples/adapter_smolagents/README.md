# thirdweb-ai with SmolAgents

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [SmolAgents](https://github.com/huggingface/smolagents), a lightweight framework for building AI agents.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with SmolAgents to create a lightweight, efficient agent for blockchain interactions.

The example creates a SmolAgents ToolCallingAgent with thirdweb's blockchain tools, enabling natural language interactions with blockchain data while maintaining a small footprint and minimal dependencies.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[smolagents]"

# Using Poetry
poetry add "thirdweb-ai[smolagents]"
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
- Query on-chain data through natural language

## Customization

You can customize the agent by modifying the example code:
- Change the LLM model using a different SmolAgents model implementation
- Adjust the `max_steps` parameter to control agent iterations
- Add different types of queries to the `queries` list
- Configure specific blockchain networks by changing the `chain_id` parameter

## Requirements

See `pyproject.toml` for the full list of dependencies. 