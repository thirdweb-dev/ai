# Modified from autogen-core (https://github.com/microsoft/autogen/blob/main/python/packages/autogen-core/src/autogen_core/tools/_base.py)

import functools
import inspect
import typing
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping, Sequence
from typing import (
    Annotated,
    Any,
    Generic,
    NotRequired,
    Protocol,
    TypedDict,
    TypeVar,
    cast,
    get_args,
    get_origin,
    runtime_checkable,
)

import jsonref
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined

TOOL_FUNCTION_ATTR_KEY = "__TOOL_FUNCTION"


def normalize_annotated_type(type_hint: type[Any]) -> type[Any]:
    """Normalize typing.Annotated types to the inner type."""
    if get_origin(type_hint) is Annotated:
        return get_args(type_hint)[0]
    return type_hint


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """Get the signature of a function with type annotations.

    Args:
        call: The function to get the signature for

    Returns:
        The signature of the function with type annotations
    """
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    func_call = call.func if isinstance(call, functools.partial) else call
    type_hints = typing.get_type_hints(func_call, globalns, include_extras=True)
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=type_hints.get(param.name, inspect.Parameter.empty),
        )
        for param in signature.parameters.values()
    ]
    return_annotation = type_hints.get("return", inspect.Signature.empty)
    return inspect.Signature(typed_params, return_annotation=return_annotation)


def type2description(k: str, v: Annotated[type[Any], str] | type[Any]) -> str:
    if hasattr(v, "__metadata__"):
        retval = v.__metadata__[0]
        if isinstance(retval, str):
            return retval
        raise ValueError(f"Invalid description {retval} for parameter {k}, should be a string.")
    return k


def args_base_model_from_signature(name: str, sig: inspect.Signature) -> type[BaseModel]:
    fields: dict[str, tuple[type[Any], Any]] = {}
    for param_name, param in sig.parameters.items():
        # This is handled externally
        if param_name == "cancellation_token" or param_name == "self":
            continue

        if param.annotation is inspect.Parameter.empty:
            raise ValueError("No annotation")

        _type = normalize_annotated_type(param.annotation)
        description = type2description(param_name, param.annotation)
        default_value = param.default if param.default is not inspect.Parameter.empty else PydanticUndefined

        fields[param_name] = (_type, Field(default=default_value, description=description))

    return cast(BaseModel, create_model(name, **fields))  # type: ignore # noqa: PGH003


class ParametersSchema(TypedDict):
    type: str
    properties: dict[str, Any]
    required: NotRequired[Sequence[str]]
    additionalProperties: NotRequired[bool]


class ToolSchema(TypedDict):
    parameters: NotRequired[ParametersSchema]
    name: str
    description: NotRequired[str]
    strict: NotRequired[bool]


@runtime_checkable
class Tool(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def schema(self) -> ToolSchema: ...

    @property
    def strict(self) -> bool: ...

    def args_type(self) -> type[BaseModel]: ...

    def return_type(self) -> type[Any]: ...

    def return_value_as_string(self, value: Any) -> str: ...

    def run_json(self, args: Mapping[str, Any]) -> Any: ...


ArgsT = TypeVar("ArgsT", bound=BaseModel, contravariant=True)
ReturnT = TypeVar("ReturnT", bound=BaseModel, covariant=True)


class BaseTool(ABC, Tool, Generic[ArgsT, ReturnT]):
    def __init__(
        self,
        args_type: type[ArgsT],
        return_type: type[ReturnT],
        name: str,
        description: str,
        strict: bool = False,
    ) -> None:
        self._args_type = args_type
        self._return_type = normalize_annotated_type(return_type)
        self._name = name
        self._description = description
        self._strict = strict

    @property
    def schema(self) -> ToolSchema:
        model_schema: dict[str, Any] = self._args_type.model_json_schema()
        if "$defs" in model_schema:
            model_schema = cast(dict[str, Any], jsonref.replace_refs(obj=model_schema, proxies=False))
            del model_schema["$defs"]

        parameters = ParametersSchema(
            type="object",
            properties=model_schema["properties"],
            required=model_schema.get("required", []),
            additionalProperties=model_schema.get("additionalProperties", False),
        )

        # If strict is enabled, the tool schema should list all properties as required.
        assert "required" in parameters
        if self._strict and set(parameters["required"]) != set(parameters["properties"].keys()):
            raise ValueError(
                "Strict mode is enabled, but not all input arguments are marked as required. Default arguments are not allowed in strict mode."
            )

        assert "additionalProperties" in parameters
        if self._strict and parameters["additionalProperties"]:
            raise ValueError(
                "Strict mode is enabled but additional argument is also enabled. This is not allowed in strict mode."
            )

        return ToolSchema(
            name=self._name,
            description=self._description,
            parameters=parameters,
            strict=self._strict,
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def strict(self) -> bool:
        return self._strict

    def args_type(self) -> type[BaseModel]:
        return self._args_type

    def return_type(self) -> type[Any]:
        return self._return_type

    def return_value_as_string(self, value: Any) -> str:
        if isinstance(value, BaseModel):
            return value.model_dump_json()

        return str(value)

    @abstractmethod
    def run(self, args: ArgsT | None = None) -> ReturnT: ...

    def run_json(self, args: Mapping[str, Any]) -> Any:
        return self.run(self._args_type.model_validate(args))


class FunctionTool(BaseTool[BaseModel, BaseModel]):
    def __init__(
        self,
        func_definition: Callable[..., Any],
        func_execute: Callable[..., Any],
        description: str,
        name: str | None = None,
        strict: bool = False,
    ) -> None:
        self._func_definition = func_definition
        self._signature = get_typed_signature(func_definition)
        self._executor = func_execute
        func_name = (
            name or func_definition.func.__name__
            if isinstance(func_definition, functools.partial)
            else name or func_definition.__name__
        )
        args_model = args_base_model_from_signature(func_name + "args", self._signature)
        return_type = self._signature.return_annotation
        super().__init__(args_model, return_type, func_name, description, strict)

    def run(self, args: BaseModel | None = None) -> Any:
        kwargs = {}

        if args:
            for name in self._signature.parameters:
                if hasattr(args, name):
                    kwargs[name] = getattr(args, name)

        return self._executor(**kwargs)


def tool(description: str | None = None, name: str | None = None, strict: bool = False) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]):
        func_name = name or func.func.__name__ if isinstance(func, functools.partial) else name or func.__name__
        func_description = description or func.__doc__
        if not func_description:
            raise ValueError("Tool description is required")

        @functools.wraps(func)
        def wrapper(cls: Any):
            return FunctionTool(
                func_definition=func,
                func_execute=lambda _cls=cls, *args, **kwargs: func(_cls, *args, **kwargs),
                description=func_description,
                name=func_name,
                strict=strict,
            )

        setattr(wrapper, TOOL_FUNCTION_ATTR_KEY, wrapper)

        return wrapper

    return decorator
