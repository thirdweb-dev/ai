import pytest
from pydantic import BaseModel, Field

from thirdweb_ai.tools.tool import BaseTool, FunctionTool, Tool


class TestArgsModel(BaseModel):
    """Test arguments model."""

    param1: str = Field(description="Test parameter 1")
    param2: int = Field(description="Test parameter 2")


class TestReturnModel(BaseModel):
    """Test return model."""

    result: str


class TestBaseTool(BaseTool[TestArgsModel, TestReturnModel]):
    """A simple test tool for testing adapters."""

    def __init__(self):
        super().__init__(
            args_type=TestArgsModel,
            return_type=TestReturnModel,
            name="test_tool",
            description="A test tool for testing",
        )

    def run(self, args: TestArgsModel | None = None) -> TestReturnModel:
        if args is None:
            raise ValueError("Arguments are required")
        return TestReturnModel(result=f"Executed with {args.param1} and {args.param2}")


@pytest.fixture
def test_tool() -> TestBaseTool:
    """Fixture that returns a test tool."""
    return TestBaseTool()


@pytest.fixture
def test_function_tool() -> FunctionTool:
    """Fixture that returns a test function tool."""

    def test_func(param1: str, param2: int = 42) -> str:
        """A test function for the function tool."""
        return f"Function called with {param1} and {param2}"

    return FunctionTool(
        func_definition=test_func,
        func_execute=test_func,
        description="A test function tool",
        name="test_function_tool",
    )


@pytest.fixture
def test_tools(test_tool: TestBaseTool, test_function_tool: FunctionTool) -> list[Tool]:
    """Fixture that returns a list of test tools."""
    return [test_tool, test_function_tool]
