import os

from mcp.server.fastmcp import FastMCP
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.mcp import add_fastmcp_tools


def main():
    """
    Example of using thirdweb_ai with MCP (Model Control Protocol) Server.

    This creates a server that provides blockchain tools via the MCP protocol,
    which can be used by compatible LLM clients.
    """

    # Initialize Thirdweb Insight and Nebula with API key
    insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
    nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))

    # Create the MCP server with thirdweb tools
    mcp = FastMCP("Thirdweb MCP", port=8000)

    # Add thirdweb tools to the MCP server
    all_tools = insight.get_tools() + nebula.get_tools()
    add_fastmcp_tools(mcp, all_tools)

    print("Starting MCP server with thirdweb tools on port 8001...")
    print("Available tools:")
    for tool in all_tools:
        print(f"- {tool.name}: {tool.description}")

    print(
        "\nConnect to this server with an MCP-compatible client and try queries like:"
    )
    print("- 'What are the addresses associated to thirdweb.eth?'")
    print("- 'What's the current balance of thirdweb.eth?'")
    print("\nPress Ctrl+C to stop the server.")

    # Start the server in SSE (Server-Sent Events) mode
    mcp.run("sse")


if __name__ == "__main__":
    main()
