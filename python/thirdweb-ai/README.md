# thirdweb-ai

[![PyPI version](https://img.shields.io/pypi/v/thirdweb-ai.svg)](https://pypi.org/project/thirdweb-ai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/thirdweb-ai.svg)](https://pypi.org/project/thirdweb-ai/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Overview

thirdweb-ai enables developers to build smarter onchain AI agents by giving them access to thirdweb's powerful web3 tools. This library seamlessly integrates with popular AI agent frameworks, allowing you to enhance your AI agents with blockchain capabilities.

With thirdweb-ai, your AI agents can:
- Deploy and interact with smart contracts
- Manage wallets and transactions
- Retrieve on-chain data
- Store and retrieve data on decentralized storage (IPFS)
- Access thirdweb's suite of web3 services

## Installation

Install the core package:

```bash
pip install thirdweb-ai[all]
```


### Install with framework-specific adapters

thirdweb-ai supports integration with several popular AI agent frameworks. You can install the package with specific extras to enable these integrations:

```bash
# Install with all adapters
pip install "thirdweb-ai[all]"

# Install with specific adapters
pip install "thirdweb-ai[openai]"  # For OpenAI Assistants
pip install "thirdweb-ai[langchain]"  # For LangChain
pip install "thirdweb-ai[autogen]"  # For AutoGen
pip install "thirdweb-ai[llama-index]"  # For LlamaIndex
pip install "thirdweb-ai[goat]"  # For GOAT
pip install "thirdweb-ai[agentkit]"  # For Coinbase AgentKit
pip install "thirdweb-ai[mcp]"  # For MCP
pip install "thirdweb-ai[smolagents]"  # For SmoLAgents
pip install "thirdweb-ai[pydantic-ai]"  # For Pydantic AI
```

## Usage

thirdweb-ai provides a set of tools that can be integrated with various AI agent frameworks. Here's a basic example:

```python
from thirdweb_ai import Engine, EngineCloud, Insight, Nebula, Storage, Tool

# Initialize thirdweb services
insight = Insight(secret_key=...)
nebula = Nebula(secret_key=...)
engine = Engine(secret_key=...)
engine_cloud = EngineCloud(secret_key=..., vault_access_token=...)  # vault_access_token required for server wallet operations
storage = Storage(secret_key=...)

# Get available tools
tools = [
    # Add the tools you need
    # e.g., contract deployment, wallet management, transaction tools, etc.
    *insight.get_tools(),
    *nebula.get_tools(),
    *engine.get_tools(),
    *engine_cloud.get_tools(),  # Use EngineCloud for cloud-based engine operations
    *storage.get_tools(),
    # Or pick an individual tool from the services
]
```

### Available Services

thirdweb-ai provides several core services:

- **Engine**: Deploy contracts, manage wallets, execute transactions, and interact with smart contracts
- **EngineCloud**: Cloud-based engine operations for creating server wallets (with KMS integration), executing contract calls, and querying transaction history
- **Insight**: Query blockchain data, retrieve transactions, events, token balances, and contract metadata
- **Nebula**: Advanced onchain analytics and data processing
- **Storage**: Store and retrieve data using IPFS and other decentralized storage solutions

## Framework Integration

thirdweb-ai can be easily integrated with various AI agent frameworks. Below are a few examples of how to integrate with some of the supported frameworks:

### LangChain

```python
from thirdweb_ai import Tool
from thirdweb_ai.adapters.langchain import get_langchain_tools

# Initialize your thirdweb tools
tools = [...]  # List of thirdweb tools

# Convert to LangChain tools
langchain_tools = get_langchain_tools(tools)

# Use in your LangChain agent
agent = create_tool_calling_agent(tools=langchain_tools, ...)
```

### OpenAI Agents

```python
from thirdweb_ai import Tool
from thirdweb_ai.adapters.openai import get_openai_tools

# Initialize your thirdweb tools
tools = [...]  # List of thirdweb tools

# Convert to OpenAI tools
openai_tools = get_openai_tools(tools)

# Use in your OpenAI Agents
agent = Agent("thirdweb assistant", tools=openai_tools, ...)
```

### AutoGen

```python
from thirdweb_ai import Tool
from thirdweb_ai.adapters.autogen import get_autogen_tools

# Initialize your thirdweb tools
tools = [...]  # List of thirdweb tools

# Convert to AutoGen tools
autogen_tools = get_autogen_tools(tools)

# Use in your AutoGen agent
```

### More Examples

More examples are available in the examples directory that can be found [here](https://github.com/thirdweb-dev/ai/tree/main/python/examples)

## Custom Integration

If you're using a framework that isn't directly supported, you can still use thirdweb-ai by creating a custom adapter. The core `Tool` class follows a standard interface that can be adapted to most frameworks:

```python
from thirdweb_ai import Tool

def adapt_to_my_framework(tools: list[Tool]):
    # Convert thirdweb tools to your framework's format
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args_schema(),
            "execute": lambda **kwargs: tool.run_json(kwargs)
        }
        for tool in tools
    ]
```


## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Development and Testing

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/thirdweb-dev/ai.git
cd ai/python/thirdweb-ai

# Install dependencies with UV
uv sync
```

### Running tests

We use pytest for testing. You can run the tests with:

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/common/test_utils.py

# Run tests with coverage report
uv run pytest --cov=thirdweb_ai

# Run tests and generate HTML coverage report
uv run pytest --cov=thirdweb_ai --cov-report=html
```

### Linting and Type Checking

```bash
# Run the ruff linter
uv run ruff check .

# Run type checking with pyright
uv run pyright
```