# thirdweb-ai with LlamaIndex

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [LlamaIndex](https://github.com/run-llama/llama_index), a data framework for LLM applications.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with LlamaIndex to create an agent that can answer blockchain-related queries through natural language.

The example uses LlamaIndex's FunctionCallingAgent with thirdweb's tools to enable a natural language interface for blockchain data queries, including wallet balances, transaction history, and ENS resolution.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[llama_index]"

# Using Poetry
poetry add "thirdweb-ai[llama_index]"
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
- Access on-chain data through natural language

## Customization

You can customize the agent by modifying the example code:
- Change the LLM model by modifying the `OpenAI` initialization
- Adjust the `max_function_calls` parameter for more complex queries
- Enable `allow_parallel_tool_calls` for improved performance on certain queries
- Add your own custom queries to the `queries` list

## Requirements

See `pyproject.toml` for the full list of dependencies. 