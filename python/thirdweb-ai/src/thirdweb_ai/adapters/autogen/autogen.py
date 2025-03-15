from typing import Any

from autogen_core import CancellationToken
from autogen_core.tools import BaseTool as AutogenBaseTool
from pydantic import BaseModel

from thirdweb_ai import Tool


def get_autogen_tools(tools: list[Tool]):
    class WrappedTool(AutogenBaseTool[BaseModel, BaseModel]):
        def __init__(self, tool: Tool):
            self.tool = tool
            super().__init__(
                name=tool.name,
                description=tool.description,
                strict=tool.strict,
                args_type=tool.args_type(),
                return_type=tool.return_type(),
            )

        async def run(self, args: BaseModel, cancellation_token: CancellationToken) -> Any:
            return self.tool.run_json(args.model_dump())

    return [WrappedTool(tool) for tool in tools]
