from langchain_core.tools.structured import StructuredTool

from thirdweb_ai import Tool


def get_langchain_tools(tools: list[Tool]) -> list[StructuredTool]:
    return [
        StructuredTool(
            name=tool.name,
            description=tool.description,
            func=lambda _t=tool, **kwargs: _t.run_json(kwargs),
            args_schema=tool.args_type(),
        )
        for tool in tools
    ]
