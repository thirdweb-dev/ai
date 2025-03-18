import inspect
from collections.abc import Callable
from typing import Any

import httpx

from thirdweb_ai.tools.tool import TOOL_FUNCTION_ATTR_KEY, Tool


class Service:
    def __init__(self, base_url: str, secret_key: str, httpx_client: httpx.Client | None = None):
        self.base_url = base_url
        self.secret_key = secret_key
        self.client = (
            httpx_client if httpx_client else httpx.Client(timeout=120.0, transport=httpx.HTTPTransport(retries=5))
        )

    def _make_headers(self):
        kwargs = {"Content-Type": "application/json"}
        if self.secret_key:
            kwargs["X-Secret-Key"] = self.secret_key
        return kwargs

    def _get(self, path: str, params: dict[str, Any] | None = None, headers: dict[str, Any] | None = None):
        path = path.lstrip("/")
        _headers = {**headers, **self._make_headers()} if headers else self._make_headers()
        response = self.client.get(f"{self.base_url}/{path}", params=params, headers=_headers)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, data: dict[str, Any] | None = None, headers: dict[str, Any] | None = None):
        path = path.lstrip("/")
        _headers = {**headers, **self._make_headers()} if headers else self._make_headers()
        response = self.client.post(f"{self.base_url}/{path}", json=data, headers=_headers)
        response.raise_for_status()
        return response.json()

    def get_tools(self) -> list[Tool]:
        tools: list[Tool] = []
        for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
            _tool = getattr(method, TOOL_FUNCTION_ATTR_KEY, None)
            if _tool and isinstance(_tool, Callable):
                tools.append(_tool(self))
        return tools
