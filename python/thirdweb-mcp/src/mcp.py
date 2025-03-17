import os

import click
from mcp.server.fastmcp import FastMCP
from thirdweb_ai import Engine, Insight, Nebula
from thirdweb_ai.adapters.mcp import add_fastmcp_tools


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Communication protocol for the MCP server. Use 'stdio' for standard input/output (default, suitable for CLI integrations) or 'sse' for Server-Sent Events (web-based applications).",
)
@click.option(
    "-p",
    "--port",
    type=int,
    default=8000,
    help="Port number for the MCP SSE server when using the 'sse' transport. Only relevant when transport is set to 'sse'. Default is 8000.",
)
@click.option(
    "-k",
    "--secret-key",
    type=str,
    default=lambda: os.getenv("THIRDWEB_SECRET_KEY"),
    help="Your thirdweb API secret key for authentication. Required for nebula and insight services. Can be obtained from the thirdweb dashboard. Falls back to THIRDWEB_SECRET_KEY environment variable if not specified.",
)
@click.option(
    "--chain-id",
    type=int,
    multiple=True,
    required=False,
    default=lambda: os.getenv("THIRDWEB_CHAIN_ID"),
    help="Blockchain network IDs to connect to (e.g., 1 for Ethereum mainnet, 137 for Polygon). Multiple chain IDs can be specified to support cross-chain operations. Required for insight when querying blockchain data.",
)
@click.option(
    "--engine-url",
    type=str,
    default=lambda: os.getenv("THIRDWEB_ENGINE_URL"),
    help="URL endpoint for thirdweb Engine service. Required when the 'engine' service is enabled. Falls back to THIRDWEB_ENGINE_URL environment variable if not specified.",
)
@click.option(
    "--engine-auth-jwt",
    type=str,
    default=lambda: os.getenv("THIRDWEB_ENGINE_AUTH_JWT"),
    help="Authentication JWT token for accessing thirdweb Engine service. Required when the 'engine' service is enabled. Falls back to THIRDWEB_ENGINE_AUTH_JWT environment variable if not specified.",
)
@click.option(
    "--engine-backend-wallet-address",
    type=str,
    default=lambda: os.getenv("THIRDWEB_ENGINE_BACKEND_WALLET_ADDRESS"),
    help="Wallet address used by the Engine backend for transactions. Optional for the 'engine' service. Falls back to THIRDWEB_ENGINE_BACKEND_WALLET_ADDRESS environment variable if not specified.",
)
def main(
    port: int,
    transport: str,
    secret_key: str,
    chain_id: list[int],
    engine_url: str,
    engine_auth_jwt: str,
    engine_backend_wallet_address: str | None,
):
    mcp = FastMCP("thirdweb MCP", port=port)

    chain_ids = [int(chain_id) for chain_id in chain_id]

    # determine which services to enable based on the provided options
    services = []
    if secret_key:
        services.extend(["nebula", "insight"])

    if engine_url and engine_auth_jwt:
        services.append("engine")

    if not services:
        raise ValueError(
            "Please provide a thirdweb secret key through the THIRDWEB_SECRET_KEY environment variable."
        )

    # enable the tools for each service
    if "nebula" in services:
        nebula = Nebula(secret_key=secret_key)
        add_fastmcp_tools(mcp, nebula.get_tools())

    if "insight" in services:
        insight = Insight(secret_key=secret_key, chain_id=chain_ids)
        add_fastmcp_tools(mcp, insight.get_tools())

    if "engine" in services:
        engine = Engine(
            engine_url=engine_url,
            engine_auth_jwt=engine_auth_jwt,
            backend_wallet_address=engine_backend_wallet_address,
            chain_id=next(iter(chain_ids)) if chain_ids else None,
            secret_key=secret_key or "",
        )
        add_fastmcp_tools(mcp, engine.get_tools())

    mcp.run(transport)


if __name__ == "__main__":
    main()
