# Testing Guide for thirdweb-ai

This document explains the testing approach for the thirdweb-ai package.

## Overview

The thirdweb-ai package provides adapters that convert thirdweb-ai tools to various AI framework formats. Since each adapter requires a different framework dependency, the testing strategy uses conditional imports to only run tests for adapters when the required dependencies are installed.

## Test Structure

- `tests/conftest.py`: Contains fixtures that are used across tests, including:
  - `test_tool`: A basic test tool for testing adaptability
  - `test_function_tool`: A function-based test tool
  - `test_tools`: Both tools as a list for testing adapters

- `tests/adapters/`: Contains tests for each adapter:
  - Each adapter has a corresponding test file named `test_*_compat.py`
  - Tests use conditional imports to skip if required dependencies are not installed

## Running Tests

### Run all available tests:

```bash
python -m pytest
```

### Run tests for a specific adapter:

```bash
python -m pytest tests/adapters/test_langchain_compat.py
```

### Run with coverage:

```bash
python -m pytest --cov=thirdweb_ai
```

## Adding New Tests

When adding tests for a new adapter:

1. Create a test file named `test_*_compat.py` in the `tests/adapters/` directory
2. Use conditional imports to check if dependencies are available:

```python
import pytest
import importlib.util

def has_module(module_name):
    """Check if module is available."""
    return importlib.util.find_spec(module_name) is not None

# Skip if the required dependency is not installed
dependency_installed = has_module("dependency_name")

@pytest.mark.skipif(not dependency_installed, reason="dependency_name not installed")
def test_your_function(test_tools):
    # Only runs if dependency is installed
    from dependency_name import SomeClass
    # Test code here
```

## Dependencies for Testing

To test a specific adapter, install the required dependency:

```bash
# For LangChain adapter
uv add langchain-core

# For LlamaIndex adapter
uv add llama-index-core

# For all dependencies
uv add -e all
```

## Test Coverage

Tests should cover:

1. Creating adapter tools from thirdweb tools
2. Verifying that properties are preserved (name, description, etc.)
3. Checking that tool execution works correctly

## Template Files

Some adapter test files are provided as `.py.template` files. These contain the test structure but are not executed by default since they require dependencies. To use them:

1. Rename from `.py.template` to `_compat.py`
2. Install the required dependency
3. Run the tests