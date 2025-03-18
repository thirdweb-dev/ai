import mcp.types as types
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools.base import Tool as FastMCPTool
from mcp.server.fastmcp.utilities.func_metadata import func_metadata
from thirdweb_ai import Tool


def get_fastmcp_tools(tools: list[Tool]) -> list[FastMCPTool]:
    return [
        FastMCPTool(
            fn=lambda _t=tool, **kwargs: _t.run_json(kwargs),
            name=tool.name,
            description=tool.description,
            parameters=tool.schema.get("parameters"),
            fn_metadata=func_metadata(tool._func_definition, skip_names=["self"]),  # noqa: SLF001
            is_async=False,
            context_kwarg=None,
        )
        for tool in tools
    ]


def add_fastmcp_tools(fastmcp: FastMCP, tools: list[Tool]):
    for tool in get_fastmcp_tools(tools):
        fastmcp._tool_manager._tools[tool.name] = tool  # noqa: SLF001


def get_mcp_tools(tools: list[Tool]) -> list[types.Tool]:
    return [
        types.Tool(
            name=tool.name,
            description=tool.description,
            inputSchema=tool.schema.get("parameters"),
        )
        for tool in tools
    ]
