from llama_index.core.tools import FunctionTool, ToolMetadata
from thirdweb_ai import Tool


def get_llama_index_tools(tools: list[Tool], return_direct: bool = False) -> list[FunctionTool]:
    return [
        FunctionTool.from_defaults(
            name=tool.name,
            description=tool.description,
            fn=lambda _t=tool, **kwargs: _t.run_json(kwargs),
            fn_schema=tool.args_type(),
            tool_metadata=ToolMetadata(
                name=tool.name, description=tool.description, fn_schema=tool.args_type(), return_direct=return_direct
            ),
        )
        for tool in tools
    ]
