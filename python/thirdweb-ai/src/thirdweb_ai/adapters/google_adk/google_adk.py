from typing import Any

from google.adk.tools import BaseTool, ToolContext
from google.genai import types

from thirdweb_ai.tools.tool import Tool, ToolSchema

from pydantic import BaseModel

class GoogleAdkTool(BaseTool):
    """Adapter for Thirdweb Tool to Google ADK BaseTool.

    This allows Thirdweb tools to be used with Google ADK agents.
    """

    def __init__(self, tool: Tool):
        """Initialize the Google ADK Tool wrapper.

        Args:
            tool: The Thirdweb Tool to wrap
        """
        self.tool = tool
        super().__init__(
            name=tool.name,
            description=tool.description,
        )

    @property
    def schema(self) -> ToolSchema:
        """Return the schema for the tool.

        Returns:
            The schema for the function declaration
        """
        return self.tool.schema

    def _get_declaration(self) -> types.FunctionDeclaration:
        """Generate the function declaration for Google ADK.

        Returns:
            A FunctionDeclaration for Google ADK
        """
        # Deep copy the parameters to avoid modifying the original
        import copy
        parameters = copy.deepcopy(self.tool.schema["parameters"])
        
        if "additionalProperties" in parameters:
            del parameters["additionalProperties"]
        
        def remove_additional_properties(obj: dict[str, Any]):
            if "additionalProperties" in obj:
                del obj["additionalProperties"]
                
            if "items" in obj and isinstance(obj["items"], dict):
                remove_additional_properties(obj["items"])
            
            if "properties" in obj and isinstance(obj["properties"], dict):
                for prop in obj["properties"].values():
                    if isinstance(prop, dict):
                        remove_additional_properties(prop)
        
        if "properties" in parameters:
            for prop in parameters["properties"].values():
                remove_additional_properties(prop)
        
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=parameters,
        )

    # Override the method with the expected signature based on the error message
    # and adapting from the reference implementation
    async def run_async(self, args: dict[str, Any], tool_context: ToolContext) -> Any:
        """Execute the tool asynchronously.

        This method adapts the Thirdweb tool to work with Google ADK's async execution.

        Returns:
            The result of running the tool
        """
        return self.tool.run_json(args)


def get_google_adk_tools(tools: list[Tool]) -> list[BaseTool]:
    """Convert Thirdweb tools to Google ADK tools.

    Args:
        tools: List of Thirdweb tools to convert

    Returns:
        List of Google ADK tools
    """
    return [GoogleAdkTool(tool) for tool in tools]
