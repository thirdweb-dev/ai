import logging
from typing import Any

from smolagents import Tool as SmolagentTool
from thirdweb_ai import Tool

logger = logging.getLogger(__name__)


def get_smolagents_tools(tools: list[Tool]) -> list[SmolagentTool]:
    class SmolTool(SmolagentTool):
        skip_forward_signature_validation = True

        def __init__(self, tool: Tool):
            self.tool = tool
            # TODO: smolagents doesn't handle anyOf types, so we need to convert them to a single type
            inputs = tool.schema.get("parameters", {}).get("properties", {})
            for key, value in inputs.items():
                anyof = value.get("anyOf", [])
                if anyof:
                    types = [x["type"] for x in anyof if x["type"] != "null"]
                    inputs[key]["type"] = types[0]
                    if len(types) > 1:
                        logger.debug(f"anyOf not implemented yet. {tool.name} on {key}: {anyof}")
            self.name = tool.name
            self.description = tool.description
            self.inputs = inputs
            self.output_type = "string"
            self.is_initialized = True

        def forward(self, **kwargs: Any):
            return self.tool.return_value_as_string(self.tool.run_json(kwargs))

    return [SmolTool(t) for t in tools]
