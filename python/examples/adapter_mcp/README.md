# thirdweb-ai with Model Control Protocol (MCP)

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with the [Model Control Protocol (MCP)](https://github.com/modelcontextprotocol/python-sdk), a standard for model-agnostic tools and function calling.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to create an MCP server that exposes thirdweb's blockchain tools, allowing any MCP-compatible client to interact with blockchain data through natural language.

The example sets up an MCP server with thirdweb's tools, enabling client applications to query blockchain data, resolve ENS names, check balances, and more through a standardized protocol.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[mcp]"

# Using Poetry
poetry add "thirdweb-ai[mcp]"
```

## Usage

1. Set your thirdweb API key as an environment variable:
```bash
export THIRDWEB_SECRET_KEY=your_api_key_here
```

2. Run the example to start the MCP server:
```bash
python example.py
```

3. Connect to the server with any MCP-compatible client and try queries like:
   - "What's the current balance of thirdweb.eth?"
   - "When is the most recent transaction of thirdweb.eth?"

## Customization

You can customize the MCP server by modifying the example code:
- Change the port number to run on a different port
- Add more thirdweb tools or custom tools
- Modify the server name
- Configure specific blockchain networks by changing the `chain_id` parameter

## Requirements

See `pyproject.toml` for the full list of dependencies. 