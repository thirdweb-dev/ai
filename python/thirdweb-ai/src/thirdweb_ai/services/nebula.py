from typing import Annotated, Any

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class Nebula(Service):
    def __init__(self, secret_key: str):
        super().__init__(base_url="https://nebula-api.thirdweb.com", secret_key=secret_key)

    @tool(
        description="Send a message to Nebula AI and get a response. This can be used for blockchain queries, contract interactions, and access to thirdweb tools."
    )
    def chat(
        self,
        message: Annotated[
            str,
            "The natural language message to process. Can be a question about blockchain data, a request to execute a transaction, or any web3-related query.",
        ],
        session_id: Annotated[
            str | None,
            "Optional session ID to maintain conversation context. If provided, this message will be part of an ongoing conversation; if omitted, a new session is created.",
        ] = None,
        context: Annotated[
            dict[str, Any] | None,
            "Contextual information for processing the request, including: chainIds (array of chain identifiers) and walletAddress (user's wallet for transaction signing). Example: {'chainIds': ['1', '137'], 'walletAddress': '0x123...'}",
        ] = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"message": message, "stream": False}
        if session_id:
            data["session_id"] = session_id
        if context:
            data["context"] = context

        return self._post("/chat", data)

    @tool(
        description="Retrieve all available Nebula AI sessions for the authenticated account. Returns an array of session metadata including IDs, titles, and creation timestamps, allowing you to find and reference existing conversations."
    )
    def list_sessions(self) -> dict[str, Any]:
        return self._get("session/list")

    @tool(
        description="Fetch complete information about a specific Nebula AI session, including conversation history, context settings, and metadata. Use this to examine past interactions or resume an existing conversation thread."
    )
    def get_session(
        self,
        session_id: Annotated[
            str,
            "Unique identifier for the target session. This UUID references a specific conversation history in the Nebula system.",
        ],
    ) -> dict[str, Any]:
        return self._get(f"/session/{session_id}")
