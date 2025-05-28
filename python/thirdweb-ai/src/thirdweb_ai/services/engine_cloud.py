# At the top of the file, add:
from typing import Annotated, Any, Literal, TypedDict

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class FilterField(TypedDict):
    field: Literal["id", "batchIndex", "from", "signerAddress", "smartAccountAddress", "chainId"]


class FilterValues(TypedDict):
    values: list[int]


class FilterOperator(TypedDict):
    operator: Literal["AND", "OR"]


FilterCondition = FilterField | FilterValues | FilterOperator


class EngineCloud(Service):
    def __init__(
        self,
        secret_key: str,
        vault_access_token: str,
    ):
        super().__init__(base_url="https://engine.thirdweb.com/v1", secret_key=secret_key)
        self.vault_access_token = vault_access_token

    def _make_headers(self):
        headers = super()._make_headers()
        if self.vault_access_token:
            headers["x-vault-access-token"] = self.vault_access_token
        return headers

    @tool(
        description="Create a new engine server wallet. This is a helper route for creating a new EOA with your KMS provider, provided as a convenient alternative to creating an EOA directly with your KMS provider."
    )
    def create_server_wallet(
        self,
        label: Annotated[
            str,
            "A human-readable label to identify this wallet.",
        ],
    ) -> dict[str, Any]:
        payload = {"label": label}
        return self._post("accounts", payload)

    @tool(
        description="Call a write function on a contract. This endpoint allows you to execute state-changing functions on smart contracts, with support for various execution strategies."
    )
    def write_contract(
        self,
        from_address: Annotated[
            str,
            "The address of the account to send the transaction from. Can be the address of a smart account or an EOA.",
        ],
        chain_id: Annotated[
            int,
            "The numeric blockchain network ID where the contract is deployed (e.g., '1' for Ethereum mainnet, '137' for Polygon).",
        ],
        method: Annotated[str, "The name of the contract function to call on the contract."],
        params: Annotated[list[Any], "The arguments to pass to the contract function."],
        contract_address: Annotated[str, "The address of the smart contract to interact with."],
        abi: Annotated[list[dict[str, Any]], "The ABI (Application Binary Interface) of the contract."],
        value: Annotated[str, "The amount of native currency to send with the transaction (in wei)."] = "0",
    ) -> dict[str, Any]:
        payload = {
            "executionOptions": {
                "from": from_address,
                "chainId": chain_id,
            },
            "params": [
                {
                    "method": method,
                    "params": params,
                    "contractAddress": contract_address,
                    "abi": abi,
                    "value": value,
                }
            ],
        }
        return self._post("write/contract", payload)

    @tool(
        description="Send an encoded transaction or a batch of transactions. This endpoint allows you to execute low-level transactions with raw transaction data."
    )
    def send_transaction(
        self,
        from_address: Annotated[str, "The address of the account to send the transaction from."],
        chain_id: Annotated[
            int,
            "The numeric blockchain network ID where the transaction will be sent (e.g., '1' for Ethereum mainnet, '137' for Polygon).",
        ],
        to_address: Annotated[
            str,
            "The recipient address for the transaction.",
        ],
        data: Annotated[
            str,
            "The encoded transaction data (hexadecimal).",
        ],
        value: Annotated[
            str,
            "The amount of native currency to send with the transaction (in wei).",
        ] = "0",
    ) -> dict[str, Any]:
        payload = {
            "executionOptions": {
                "from": from_address,
                "chainId": chain_id,
            },
            "params": [
                {
                    "to": to_address,
                    "data": data,
                    "value": value,
                }
            ],
        }

        return self._post("write/transaction", payload)

    @tool(
        description="Call read-only contract functions or batch read using multicall. This is a gas-efficient way to query data from blockchain contracts without modifying state."
    )
    def read_contract(
        self,
        multicall_address: Annotated[
            str | None,
            "Optional multicall contract address for batching multiple calls. Defaults to the default multicall3 address for the chain",
        ],
        chain_id: Annotated[
            int,
            "The numeric blockchain network ID where the contract is deployed (e.g., '1' for Ethereum mainnet, '137' for Polygon).",
        ],
        from_address: Annotated[str, "EVM address in hex format"],
        method: Annotated[str, "The name of the contract function to call."],
        params: Annotated[list[Any], "The arguments to pass to the contract function."],
        contract_address: Annotated[
            str,
            "The address of the smart contract to read from.",
        ],
        abi: Annotated[list[dict[str, Any]], "The ABI (Application Binary Interface) for the contract."],
    ) -> dict[str, Any]:
        payload = {
            "readOptions": {
                "multicallAddress": multicall_address,
                "chainId": chain_id,
                "from": from_address,
            },
            "params": [
                {
                    "method": method,
                    "params": params,
                    "contractAddress": contract_address,
                    "abi": abi,
                }
            ],
        }

        return self._post("read/contract", payload)

    @tool(
        description="Fetch the native cryptocurrency balance (e.g., ETH, MATIC) for a given address on a specific blockchain."
    )
    def get_native_balance(
        self,
        chain_id: Annotated[
            int,
            "The numeric blockchain network ID to query (e.g., '1' for Ethereum mainnet, '137' for Polygon).",
        ],
        address: Annotated[str, "The wallet address to check the balance for."],
    ) -> dict[str, Any]:
        payload = {
            "chainId": chain_id,
            "address": address,
        }

        return self._post("read/balance", payload)

    @tool(
        description="Search for transactions with flexible filtering options. Retrieve transaction history with customizable filters for addresses, chains, statuses, and more."
    )
    def search_transactions(
        self,
        filters: Annotated[FilterField, "List of filter conditions to apply"],
        filters_operation: Annotated[
            Literal["AND", "OR"],
            "Logical operation to apply between filters. 'AND' means all conditions must match, 'OR' means any condition can match.",
        ] = "AND",
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 1.",
        ] = 1,
        limit: Annotated[
            int | None,
            "Maximum number of transactions to return per page (1-100).",
        ] = 20,
        sort_by: Annotated[
            Literal["createdAt", "confirmedAt"],
            "Field to sort results by.",
        ] = "createdAt",
        sort_direction: Annotated[
            Literal["asc", "desc"],
            "Sort direction ('asc' for ascending, 'desc' for descending).",
        ] = "desc",
    ) -> dict[str, Any]:
        payload = {
            "filters": filters,
            "filtersOperation": filters_operation,
            "page": page,
            "limit": limit,
            "sortBy": sort_by,
            "sortDirection": sort_direction,
        }

        return self._post("transactions/search", payload)

    @tool(
        description="List all engine server wallets for the current project. Returns an array of EOA addresses with their corresponding predicted smart account addresses."
    )
    def get_accounts(self) -> dict[str, Any]:
        """Get all engine server wallets for the current project.

        Returns:
            dict containing list of account objects with address and smartAccountAddress
        """
        return self._get("accounts")
