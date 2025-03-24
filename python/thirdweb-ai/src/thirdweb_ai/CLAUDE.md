# thirdweb-ai Development Guide

## Commands

- Install: `pip install -e .`
- Lint: `ruff check --fix .`
- Type check: `mypy .`
- Run test: `pytest tests/`
- Run single test: `pytest tests/path/to/test.py::TestClass::test_method -v`

## Code Style

- **Imports**: Standard library first, third-party second, local imports third
- **Type Hints**: Use type hints for all parameters and return values (e.g. `int | str`, `list[str]`)
- **Documentation**: Use descriptive Annotated hints for parameters
- **Naming**:
  - Classes: PascalCase (e.g. `Engine`, `Insight`)
  - Functions/Variables: snake_case (e.g. `normalize_chain_id`)
  - Constants: UPPER_SNAKE_CASE
- **Error Handling**: Use specific exceptions with descriptive messages
- **Chain IDs**: Allow both `str` and `int` types, use `normalize_chain_id()` function
- **Parameter Validation**: Validate function inputs at the start of the function

## Functionality

Adapters are organized by framework, services connect to thirdweb backends (Engine, Insight, etc.).