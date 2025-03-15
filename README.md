# thirdweb AI

_AI Agents with Onchain Intelligence_

## 📖 Overview

thirdweb AI is thirdweb's comprehensive toolkit for blockchain data analysis, wallet management, and AI-powered interaction with blockchains. It simplifies complex blockchain operations into three core components: Insight for data analysis, Engine for wallet and contract operations, and Nebula for natural language-powered blockchain interactions.

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

### Nebula
AI-powered blockchain interaction:
- **Natural Language Agent Action**: Control blockchain operations through natural language instructions

## 🚀 Quickstart

### Python

#### Installation

```bash
# Install core package
pip install "thirdweb-ai[all]"

# Or install with specific framework adapters
pip install "thirdweb-ai[openai]"    # For OpenAI Agents
pip install "thirdweb-ai[langchain]" # For LangChain
pip install "thirdweb-ai[agentkit]" # For Coinbase Agentkit
```

#### Basic Usage

```python
from thirdweb_ai import Engine, Insight, Nebula, Tool

# Initialize services
insight = Insight(secret_key=...)
nebula = Nebula(secret_key=...)
engine = Engine(...)

# Example: Create tools for AI agents
tools = [
    *insight.get_tools(),
    *nebula.get_tools(),
    *engine.get_tools(),
    # Or pick an individual tool from the services
]

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


### TypeScript

Coming soon.

## 📜 Documentation

For comprehensive documentation, please visit:

- [thirdweb Documentation](https://portal.thirdweb.com/)

## 🚨 Security and Bug Reports

We take security seriously. If you discover a security vulnerability within thirdweb AI, please email security@thirdweb.com rather than using the issue tracker.

For non-security-related bugs, please use the GitHub issue tracker.

## 📧 Contact

- **Website**: [thirdweb.com](https://thirdweb.com)
- **X**: [@thirdweb](https://x.com/thirdweb)
- **Discord**: [Join our community](https://discord.gg/thirdweb)
- **Email**: support@thirdweb.com

## 📝 License

thirdweb AI is licensed under the Apache-2.0 License. See the [LICENSE](./LICENSE) file for details.