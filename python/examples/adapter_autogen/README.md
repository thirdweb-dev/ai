# thirdweb-ai with AutoGen

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [AutoGen](https://github.com/microsoft/autogen), an open-source framework from Microsoft Research for building autonomous agents.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with AutoGen to create an AI assistant that can answer queries about blockchain data, resolve ENS names, check wallet balances, and more, all through natural language.

The example creates an AutoGen assistant agent with thirdweb's blockchain tools and demonstrates querying blockchain data, including wallet balances and transaction information.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[autogen]"

# Using Poetry
poetry add "thirdweb-ai[autogen]"
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
- Get transaction history
- Resolve ENS names

## Customization

You can customize the assistant by modifying the example code:
- Add different types of tools by extending the `tools` list
- Change the model by modifying the `model` configuration
- Add your own queries to the `queries` list

## Requirements

See `pyproject.toml` for the full list of dependencies. 