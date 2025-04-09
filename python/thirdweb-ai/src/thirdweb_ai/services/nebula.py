from typing import Annotated, Any

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class Nebula(Service):
    def __init__(
        self, secret_key: str, session_id: str | None = None, response_format: dict[str, int | str] | None = None
    ) -> None:
        super().__init__(base_url="https://nebula-api.thirdweb.com", secret_key=secret_key)
        self.response_format = response_format or None
        self.session_id = session_id or None

    @tool(
        description="Send a message to Nebula AI and get a response. This can be used for blockchain queries, contract interactions, and access to thirdweb tools."
    )
    def chat(
        self,
        message: Annotated[
            str,
            "The natural language message to process. Can be a question about blockchain data, a request to execute a transaction, or any web3-related query.",
        ],
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"message": message, "stream": False}
        if self.response_format:
            data["response_format"] = self.response_format
        if self.session_id:
            data["context"] = {"session_id": self.session_id}

        return self._post("/chat", data)

    def list_sessions(self) -> dict[str, Any]:
        return self._get("session/list")

    def get_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        return self._get(f"/session/{session_id}")

    def create_session(self) -> dict[str, Any]:
        data = {}
        return self._post("/session", data)
