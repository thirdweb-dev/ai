# thirdweb MCP Server

A Model Control Protocol (MCP) server implementation for thirdweb services integration. This server allows you to integrate thirdweb's tools with any MCP-compatible client.

## Overview

thirdweb MCP provides a unified interface to access thirdweb's suite of blockchain tools and services through the standardized Model Control Protocol. It supports multiple communication transports and can be integrated with various thirdweb services:

- **Nebula**: Autonomous onchain execution - real-time on-chain analysis, code generation and contract interactions
- **Insight**: Blockchain data analysis capabilities for real-time on-chain data
- **Engine**: Integration with thirdweb's backend infrastructure for contract deployments and interactions

## Installation

### Prerequisites

- Python 3.10 or higher
- Poetry (recommended for dependency management)

### Run with uvx
```bash
THIRDWEB_SECRET_KEY=... \
    uvx thirdweb-mcp
```

### Install and run with pipx

```bash
pipx install thirdweb-mcp

THIRDWEB_SECRET_KEY=... \
    thirdweb-mcp
```

### Install from source

```bash
git clone https://github.com/thirdweb-dev/ai.git thirdweb-ai
cd thirdweb-ai/python/thirdweb-mcp
poetry install
```

## Configuration

The thirdweb MCP server requires configuration based on which services you want to enable:

1. **thirdweb Secret Key**: Required for Nebula and Insight services. Obtain from the [thirdweb dashboard](https://thirdweb.com/dashboard).
2. **Chain IDs**: Blockchain network IDs to connect to (e.g., 1 for Ethereum mainnet, 137 for Polygon).
3. **Engine Configuration**: If using the Engine service, you'll need the Engine URL and authentication JWT.

You can provide these through command-line options or environment variables.

## Usage

### Command-line options

```bash
# Basic usage with default settings (stdio transport with Nebula and Insight)
THIRDWEB_SECRET_KEY=... thirdweb-mcp 

# Using SSE transport on a custom port
THIRDWEB_SECRET_KEY=... thirdweb-mcp --transport sse --port 8080

# Enabling all services with specific chain IDs
THIRDWEB_SECRET_KEY=... thirdweb-mcp --chain-id 1 --chain-id 137 \
    --engine-url YOUR_ENGINE_URL \
    --engine-auth-jwt YOUR_ENGINE_JWT \ 
    --engine-backend-wallet-address YOUR_ENGINE_BACKEND_WALLET_ADDRESS
```

### Environment variables

You can also configure the MCP server using environment variables:

- `THIRDWEB_SECRET_KEY`: Your thirdweb API secret key
- `THIRDWEB_ENGINE_URL`: URL endpoint for thirdweb Engine service
- `THIRDWEB_ENGINE_AUTH_JWT`: Authentication JWT token for Engine
- `THIRDWEB_ENGINE_BACKEND_WALLET_ADDRESS`: Wallet address for Engine backend

### Integration with Claude Desktop
To add this MCP server to Claude Desktop:

1. Install the MCP: `pipx install thirdweb-mcp`

2. Create or edit the Claude Desktop configuration file at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

3. Add the following configuration:

   ```json
   {
     "mcpServers": {
       "thirdweb-mcp": {
         "command": "thirdweb-mcp",
         "args": [], // add `--chain-id` optionally
         "env": {
           "THIRDWEB_SECRET_KEY": "your thirdweb secret key from dashboard",
           "THIRDWEB_ENGINE_URL": "(OPTIONAL) your engine url",
           "THIRDWEB_ENGINE_AUTH_JWT": "(OPTIONAL) your engine auth jwt",
           "THIRDWEB_ENGINE_BACKEND_WALLET_ADDRESS": "(OPTIONAL) your engine backend wallet address",           
         },
       }
     }
   }
   ```

4. Restart Claude Desktop for the changes to take effect.

Read more on [MCP Quickstart](https://modelcontextprotocol.io/quickstart/user)

### Integration with MCP clients

This server can be integrated with any client that supports the Model Control Protocol:

1. Run the MCP server with the appropriate configuration
2. Connect your MCP client to the server using the selected transport (stdio or SSE)
3. Access thirdweb services through the exposed MCP tools

## Available Services

### Nebula

Autonomous onchain execution and analysis:
- Analyze smart contract code
- Contract interactions and deployments
- Autonomous onchain tasks execution

### Insight

Offers blockchain data analysis capabilities:
- Query on-chain data across multiple networks
- Analyze transactions, blocks, and smart contract events
- Monitor wallet activities and token movements

### Engine

Integrates with thirdweb's backend infrastructure:
- Deploy smart contracts
- Interact with deployed contracts
- Manage wallet connections and transactions

## License

[Apache-2.0 License](LICENSE)

## Support

For questions or support, please contact [support@thirdweb.com](mailto:support@thirdweb.com) or visit [thirdweb.com](https://thirdweb.com).
