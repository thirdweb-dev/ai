from typing import Any, Dict

from google.adk.agents.llm_agent import ToolUnion
from google.adk.tools import BaseTool
from pydantic import BaseModel

from thirdweb_ai import Tool


def get_google_adk_tools(tools: list[Tool]) -> list[BaseTool]:
    class WrappedTool(BaseTool):
        def __init__(self, tool: Tool):
            self.tool = tool
            super().__init__(
                name=tool.name,
                description=tool.description,
            )

        async def run(self, args: BaseModel) -> Any:
            return self.tool.run_async(args.model_dump())

    return [WrappedTool(tool) for tool in tools]
