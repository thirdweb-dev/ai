# thirdweb AI

_AI Agents with Onchain Intelligence_

## 📖 Overview

thirdweb AI is thirdweb's comprehensive toolkit for blockchain data analysis, wallet management, and AI agent interaction with blockchains. It simplifies complex blockchain operations into four core components: Insight for data analysis, Engine for wallet and contract operations, Storage for decentralized file management, and Nebula for natural language-powered blockchain interactions.

## 🌐 Features

### Insight
Comprehensive blockchain data intelligence:
- **Chains**: Multi-chain support and network information
- **Transactions**: Transaction analysis and monitoring
- **Blocks**: Block data exploration and metrics
- **Events**: Smart contract event tracking and filtering
- **Prices**: Real-time token price feeds
- **Tokens**: Detailed token information and analytics

### Engine
Core blockchain interaction capabilities:
- **Wallet**: Secure wallet management and transaction signing
- **Read**: Read operations for smart contracts and blockchain data
- **Write**: Transaction creation and contract interaction

### Storage
Decentralized storage capabilities:
- **Upload**: Upload files, directories, and JSON data to IPFS
- **Fetch**: Retrieve content from IPFS using thirdweb gateway

### Nebula
AI agent blockchain interaction:
- **Natural Language Agent Action**: Completing blockchain tasks through natural language instructions

## 🚀 Quickstart

### MCP Server

#### Installation

```bash
### Run using uvx
THIRDWEB_SECRET_KEY=... \
    uvx thirdweb-mcp

### Install and run using pipx (and run thirdweb-mcp)
pipx install thirdweb-mcp

THIRDWEB_SECRET_KEY=... \
    thirdweb-mcp
```

More [information](python/thirdweb-mcp)

### Python SDK

#### Installation

```bash
# Install core package with all framework adapters
pip install "thirdweb-ai[all]"

# Or install with specific framework adapters
pip install "thirdweb-ai[openai]"    # For OpenAI Agents
pip install "thirdweb-ai[langchain]" # For LangChain
pip install "thirdweb-ai[agentkit]" # For Coinbase Agentkit
pip install "thirdweb-ai[goat]" # For GOAT SDK
# ... many more framework supported
```

See the list of [supported framework and installation guides](python/thirdweb-ai#install-with-framework-specific-adapters)

#### Basic Usage

```python
from thirdweb_ai import Engine, Insight, Nebula, Storage, Tool

# Initialize services
insight = Insight(secret_key=...)
nebula = Nebula(secret_key=...)
engine = Engine(...)
storage = Storage(secret_key=...)

# Example: Create tools for AI agents
# Option 1: Use Nebula alone (recommended when you need a self-sufficient blockchain agent)
# Nebula already uses most other services internally
tools = [
    *nebula.get_tools(),
]

# Option 2: Use individual services directly without Nebula
# tools = [
#     *insight.get_tools(),
#     *engine.get_tools(),
#     *storage.get_tools(),
# ]

# Example: Framework integration (LangChain)
from thirdweb_ai.adapters.langchain import get_langchain_tools
langchain_tools = get_langchain_tools(tools)
agent = create_tool_calling_agent(tools=langchain_tools, ...)

# Example: Framework integration (OpenAI Agents)
from thirdweb_ai.adapters.openai import get_openai_tools
openai_tools = get_openai_tools(tools)
agent = Agent(name="thirdweb Assistant", tools=tools)

# see python/examples for other framework integration
```

More [information](python/thirdweb-ai)

### TypeScript SDK

Coming soon.

## 📜 Documentation

For comprehensive documentation, please visit:

- [thirdweb Documentation](https://portal.thirdweb.com/)

## 🚨 Security and Bug Reports

We take security seriously. If you discover a security vulnerability within thirdweb AI, please email security@thirdweb.com rather than using the issue tracker.

For non-security-related bugs, please use the GitHub issue tracker.

## ⚠️ Important Usage Notes

When using Nebula, do not combine it with other tools (Insight, Engine, Storage) in the same agent implementation as Nebula already calls these tools in the background. Using them together can lead to compatibility issues and unexpected behavior.

## 📦 Publishing Workflow

To publish a new version of thirdweb AI packages:

1. Create a git tag for the new version: `git tag -a v0.X.Y -m "Release v0.X.Y"`
2. Push the tag to GitHub: `git push origin v0.X.Y`
3. Go to GitHub and create a release using this tag
4. The CI/CD pipeline will automatically build and publish both packages to PyPI with matching version numbers

## 📧 Contact

- **Website**: [thirdweb.com](https://thirdweb.com)
- **X**: [@thirdweb](https://x.com/thirdweb)
- **Telegram**: [Join our community](https://t.me/officialthirdweb)
- **Discord**: [Join our community](https://discord.gg/thirdweb)
- **Email**: support@thirdweb.com

## 📝 License

thirdweb AI is licensed under the Apache-2.0 License. See the [LICENSE](./LICENSE) file for details.
