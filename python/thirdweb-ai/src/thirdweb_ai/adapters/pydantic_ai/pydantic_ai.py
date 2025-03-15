from typing import Any

from pydantic_ai import RunContext
from pydantic_ai import Tool as PydanticTool
from pydantic_ai.tools import ToolDefinition
from thirdweb_ai import Tool


def get_pydantic_ai_tools(tools: list[Tool]) -> list[PydanticTool]:
    def _get_tool(tool: Tool):
        async def execute(**kwargs: Any) -> Any:
            return tool.run_json(kwargs)

        async def prepare(ctx: RunContext, tool_def: ToolDefinition) -> ToolDefinition:
            tool_def.parameters_json_schema = tool.schema["parameters"]
            return tool_def

        return PydanticTool(
            function=execute,
            prepare=prepare,
            name=tool.name,
            description=tool.description,
        )

    return [_get_tool(tool) for tool in tools]
