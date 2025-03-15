from typing import Annotated, Any

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class Engine(Service):
    def __init__(
        self,
        engine_url: str,
        engine_auth_jwt: str,
        chain_id: int | None = None,
        backend_wallet_address: str | None = None,
        secret_key: str = "",
    ):
        super().__init__(base_url=engine_url, secret_key=secret_key)
        self.engine_url = engine_url
        self.engine_auth_jwt = engine_auth_jwt
        self.backend_wallet_address = backend_wallet_address
        self.chain_id = str(chain_id) if chain_id else None

    @tool(
        description="Create and initialize a new backend wallet controlled by thirdweb Engine. These wallets are securely managed by the Engine service and can be used to sign blockchain transactions, deploy contracts, and execute on-chain operations without managing private keys directly."
    )
    def create_backend_wallet(
        self,
        wallet_type: Annotated[
            str,
            "The type of backend wallet to create. Currently supported options are 'local' (stored locally in Engine's database) or 'smart:local' (for smart account wallets with advanced features). Choose 'local' for standard EOA wallets, and 'smart:local' for smart contract wallets with batching capabilities.",
        ],
        label: Annotated[
            str | None,
            "Optional human-readable label to identify this wallet (e.g., 'Treasury Wallet', 'Game Rewards Wallet'). Helpful when managing multiple wallets in the Engine dashboard.",
        ] = None,
    ) -> dict[str, Any]:
        """Create a backend wallet."""
        payload = {"type": wallet_type}

        if wallet_type not in ["local", "smart:local"]:
            raise ValueError("invalid wallet type")

        if label:
            payload["label"] = label

        return self._post("backend-wallet/create", payload)

    @tool(
        description="Retrieve a list of all backend wallets managed by your thirdweb Engine instance. Use this to view wallet addresses, types, labels, and statuses to help manage and select wallets for blockchain operations."
    )
    def get_all_backend_wallet(
        self,
        page: Annotated[
            int | None,
            "The page number to retrieve, starting at 1. Use with 'limit' to paginate through large wallet lists.",
        ] = 1,
        limit: Annotated[
            int | None,
            "The maximum number of wallets to return per page (between 1-100). Lower values load faster but require more pagination.",
        ] = 20,
    ) -> dict[str, Any]:
        """Get all backend wallets."""
        return self._get("backend-wallet/get-all", params={"page": page, "limit": limit})

    @tool(
        description="Check the current balance of a backend wallet on a specific blockchain. Returns the balance in wei (smallest unit) for both native currency (ETH, MATIC, etc.) and ERC20 tokens. Essential for verifying if a wallet has sufficient funds before sending transactions."
    )
    def get_wallet_balance(
        self,
        backend_wallet_address: Annotated[
            str | None,
            "The Ethereum address of the wallet to check (e.g., '0x1234...'). If not provided, uses the default backend wallet address configured in the Engine instance.",
        ] = None,
        chain_id: Annotated[
            str | None,
            "The numeric blockchain network ID to query (e.g., '1' for Ethereum mainnet, '137' for Polygon). If not provided, uses the default chain ID configured in the Engine instance.",
        ] = None,
    ) -> dict[str, Any]:
        """Get wallet balance for native or ERC20 tokens."""
        chain_id = chain_id or self.chain_id
        backend_wallet_address = backend_wallet_address or self.backend_wallet_address
        return self._get(f"backend-wallet/{chain_id}/{backend_wallet_address}/get-balance")

    @tool(
        description="Send an on-chain transaction from a backend wallet. This powerful function can transfer native currency (ETH, MATIC), ERC20 tokens, or execute any arbitrary contract interaction. The transaction is signed and broadcast to the blockchain automatically by the Engine service."
    )
    def send_transaction(
        self,
        to_address: Annotated[
            str,
            "The recipient Ethereum address that will receive the transaction (e.g., '0x1234...'). This can be a wallet address (for transfers) or a contract address (for contract interactions).",
        ],
        value: Annotated[
            str,
            "The amount of native currency to send, specified in wei (e.g., '1000000000000000000' for 1 ETH). For token transfers or contract interactions that don't need to send value, use '0'.",
        ],
        data: Annotated[
            str | None,
            "The hexadecimal transaction data payload for contract interactions (e.g., '0x23b872dd...'). For simple native currency transfers, leave this empty. For ERC20 transfers or contract calls, this contains the ABI-encoded function call.",
        ] = None,
        backend_wallet_address: Annotated[
            str | None,
            "The sender wallet address to use (must be a wallet created through Engine). If not provided, uses the default backend wallet configured in the Engine instance.",
        ] = None,
        chain_id: Annotated[
            str | None,
            "The numeric blockchain network ID to send the transaction on (e.g., '1' for Ethereum mainnet, '137' for Polygon). If not provided, uses the default chain ID configured in the Engine instance.",
        ] = None,
    ) -> dict[str, Any]:
        """Send a transaction from a backend wallet."""

        payload = {
            "to": to_address,
            "value": value,
        }

        if data:
            payload["data"] = data

        chain_id = chain_id or self.chain_id
        backend_wallet_address = backend_wallet_address or self.backend_wallet_address
        return self._post(
            f"backend-wallet/{chain_id}/send-transaction",
            payload,
            headers={"X-Backend-Wallet-Address": backend_wallet_address},
        )

    @tool(
        description="Track the current status of a previously submitted transaction. This helps monitor if your transaction is pending, has been successfully mined and confirmed, or has failed. Essential for implementing reliable transaction flows with proper error handling."
    )
    def get_transaction_status(
        self,
        queue_id: Annotated[
            str,
            "The unique queue identifier returned when you initially submitted the transaction through Engine (e.g., '9eb88b00-f04f-409b-9df7-7dcc9003bc35'). Not the same as the on-chain transaction hash.",
        ],
    ) -> dict[str, Any]:
        """Get the status of a transaction by queue ID."""
        return self._get(f"transaction/{queue_id}")

    @tool(
        description="Call a read-only function on a smart contract to query its current state without modifying the blockchain or spending gas. Perfect for retrieving information like token balances, contract configuration, or any view/pure functions from Solidity contracts."
    )
    def read_contract(
        self,
        contract_address: Annotated[
            str,
            "The Ethereum address of the smart contract to query (e.g., '0x1234...'). Must be a deployed contract on the specified chain.",
        ],
        function_name: Annotated[
            str,
            "The exact name of the function to call on the contract (e.g., 'balanceOf', 'totalSupply'). Must match the function name in the contract's ABI exactly, including correct capitalization.",
        ],
        function_args: Annotated[
            list[Any] | None,
            "An ordered list of arguments to pass to the function (e.g., [address, tokenId]). Must match the types and order expected by the function. For functions with no parameters, use an empty list or None.",
        ] = None,
        chain_id: Annotated[
            str | None,
            "The numeric blockchain network ID where the contract is deployed (e.g., '1' for Ethereum mainnet, '137' for Polygon). If not provided, uses the default chain ID configured in the Engine instance.",
        ] = None,
    ) -> dict[str, Any]:
        """Read data from a smart contract."""
        payload = {
            "functionName": function_name,
            "args": function_args or [],
        }

        chain_id = chain_id or self.chain_id
        return self._post(f"contract/{chain_id!s}/{contract_address}/read", payload)

    @tool(
        description="Execute a state-changing function on a smart contract by sending a transaction. This allows you to modify on-chain data, such as transferring tokens, minting NFTs, or updating contract configuration. The transaction is automatically signed by your backend wallet and submitted to the blockchain."
    )
    def write_contract(
        self,
        contract_address: Annotated[
            str,
            "The Ethereum address of the smart contract to interact with (e.g., '0x1234...'). Must be a deployed contract on the specified chain.",
        ],
        function_name: Annotated[
            str,
            "The exact name of the function to call on the contract (e.g., 'mint', 'transfer', 'setApprovalForAll'). Must match the function name in the contract's ABI exactly, including correct capitalization.",
        ],
        function_args: Annotated[
            list[Any] | None,
            "An ordered list of arguments to pass to the function (e.g., ['0x1234...', 5] for transferring 5 tokens to address '0x1234...'). Must match the types and order expected by the function. For functions with no parameters, use an empty list.",
        ] = None,
        value: Annotated[
            str | None,
            "The amount of native currency (ETH, MATIC, etc.) to send with the transaction, in wei (e.g., '1000000000000000000' for 1 ETH). Required for payable functions, use '0' for non-payable functions.",
        ] = "0",
        chain_id: Annotated[
            str | None,
            "The numeric blockchain network ID where the contract is deployed (e.g., '1' for Ethereum mainnet, '137' for Polygon). If not provided, uses the default chain ID configured in the Engine instance.",
        ] = None,
    ) -> dict[str, Any]:
        """Write data to a smart contract."""
        payload: dict[str, Any] = {
            "functionName": function_name,
            "args": function_args or [],
        }

        if value:
            payload["txOverrides"] = {"value": value}

        chain_id = chain_id or self.chain_id
        return self._post(
            f"contract/{chain_id!s}/{contract_address}/write",
            payload,
            headers={"X-Backend-Wallet-Address": self.backend_wallet_address},
        )
