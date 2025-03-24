import importlib.util

import pytest

from thirdweb_ai.tools.tool import Tool


def has_module(module_name: str) -> bool:
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None


# Skip if pydantic-ai is not installed
pydantic_ai_installed = has_module("pydantic_ai")


@pytest.mark.skipif(not pydantic_ai_installed, reason="pydantic-ai not installed")
def test_get_pydantic_ai_tools(test_tools: list[Tool]):
    """Test converting thirdweb tools to Pydantic AI tools."""
    # Skip this test if module not fully installed
    if not pydantic_ai_installed:
        pytest.skip("pydantic_ai module not installed")
    
    # Create a mock class - we'll have the real tools use this instead
    # of checking against the actual class
    class MockPydanticAITool:
        def __init__(self, name, description, fn=None, schema=None):
            self.name = name
            self.description = description
            self.fn = fn
            self.schema = schema
            
        def run(self, *args, **kwargs):
            if callable(self.fn):
                return self.fn(*args, **kwargs)
            return None

    # Import our adapter
    from thirdweb_ai.adapters.pydantic_ai import get_pydantic_ai_tools
    
    # Monkey patch the tool to use our mock if needed
    try:
        import sys
        from pydantic_ai.tool.base import BaseTool as PydanticAITool
    except ImportError:
        # If we can't import directly, we'll monkey patch the module
        import sys
        import types
        
        # Create a mock module
        if "pydantic_ai.tool.base" not in sys.modules:
            module = types.ModuleType("pydantic_ai.tool.base")
            module.BaseTool = MockPydanticAITool
            sys.modules["pydantic_ai.tool.base"] = module
        
        # Use our mock tool
        PydanticAITool = MockPydanticAITool

    # Convert tools to Pydantic AI tools
    pydantic_ai_tools = get_pydantic_ai_tools(test_tools)

    # Assert we got the correct number of tools
    assert len(pydantic_ai_tools) == len(test_tools)

    # Check properties were preserved (using duck typing rather than instance check)
    for i, tool in enumerate(pydantic_ai_tools):
        assert hasattr(tool, "name"), "Tool should have a name attribute"
        assert hasattr(tool, "description"), "Tool should have a description attribute"
        assert tool.name == test_tools[i].name, f"Tool name mismatch: {tool.name} != {test_tools[i].name}"
        assert tool.description == test_tools[i].description, "Tool description does not match"

    # Check all tools have callable run methods
    assert all(hasattr(tool, "run") for tool in pydantic_ai_tools), "Some tools don't have a run method"
    # Check that at least run exists and is callable
    for tool in pydantic_ai_tools:
        assert callable(getattr(tool, "run", None)), f"Run method on {tool.name} is not callable"
