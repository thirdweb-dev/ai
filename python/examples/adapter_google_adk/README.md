# thirdweb-ai with Google Agent Development Kit (ADK)

This example demonstrates how to integrate thirdweb-ai's blockchain tooling with [Google ADK](https://github.com/google/adk-python), an open-source toolkit from Google for building autonomous agents.

## Overview

thirdweb-ai provides powerful blockchain data access and interaction tools through its Insight and Nebula services. This example shows how to use these tools with Google ADK to create an AI assistant that can answer queries about blockchain data, check wallet balances, and more, all through natural language.

## Installation

First, ensure you have Python 3.10+ installed. Then install the required packages:

```bash
# Using pip
pip install "thirdweb-ai[google-adk]"

# Using uv
uv add "thirdweb-ai[google-adk]"
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
- Get details of a transaction

## Customization

You can customize the assistant by modifying the example code:
- Add different types of tools by extending the `tools` list
- Change the model by modifying the `model` configuration
- Add your own queries

## Requirements

See `pyproject.toml` for the full list of dependencies. 
