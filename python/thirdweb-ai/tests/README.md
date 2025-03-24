# Tests for thirdweb-ai

This directory contains tests for the thirdweb-ai package.

## Structure

- `adapters/`: Tests for the adapter modules that convert thirdweb-ai tools to various AI framework formats
- `conftest.py`: Pytest fixtures and configurations

## Running Tests

Run all tests:

```bash
pytest
```

Run specific tests:

```bash
# Run tests for a specific adapter
pytest tests/adapters/test_langchain.py

# Run tests with coverage
pytest --cov=thirdweb_ai

# Run tests with more verbosity
pytest -v
```

## Test Fixtures

The `conftest.py` file provides several useful fixtures:

- `test_tool`: A basic thirdweb-ai Tool for testing
- `test_function_tool`: A FunctionTool implementation for testing
- `test_tools`: A list containing both tools for testing adapters