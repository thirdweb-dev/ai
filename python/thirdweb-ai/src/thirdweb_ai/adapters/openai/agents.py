import json
from typing import Any

from agents import FunctionTool, RunContextWrapper

from thirdweb_ai import Tool


def _get_openai_schema(schema: Any):
    if not isinstance(schema, dict):
        return None

    schema["additionalProperties"] = False

    if "properties" in schema:
        schema["required"] = list(schema["properties"].keys())
        for prop in schema["properties"].values():
            if isinstance(prop, dict):
                prop.pop("default", None)
                _get_openai_schema(prop)

    return schema


def get_agents_tools(tools: list[Tool]):
    def _get_tool(tool: Tool):
        async def _invoke_tool(ctx: RunContextWrapper[Any], tool_input: str, _t: Tool = tool) -> str:  # type: ignore # noqa: PGH003
            input_args = json.loads(tool_input) if tool_input else {}
            return _t.return_value_as_string(_t.run_json(input_args))

        schema = _get_openai_schema(tool.schema.get("parameters"))
        return FunctionTool(  # type: ignore # noqa: PGH003
            name=tool.name,
            description=tool.description,
            params_json_schema=schema,
            on_invoke_tool=_invoke_tool,
        )

    return [_get_tool(tool) for tool in tools]
