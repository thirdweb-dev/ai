from typing import Annotated, Any, Literal

from thirdweb_ai.common.address import (
    validate_address,
    validate_block_identifier,
    validate_signature,
    validate_transaction_hash,
)
from thirdweb_ai.common.utils import EVENT_KEYS_TO_KEEP, TRANSACTION_KEYS_TO_KEEP, clean_resolve, filter_response_keys
from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class Insight(Service):
    def __init__(self, secret_key: str, chain_id: int | list[int] | None = None):
        super().__init__(base_url="https://insight.thirdweb.com/v1", secret_key=secret_key)
        self.chain_ids = [chain_id or 1]

    @tool(
        description="Retrieve blockchain events with flexible filtering options. Use this to search for specific events or to analyze event patterns across multiple blocks. Do not use this tool to simply look up a single transaction."
    )
    def get_events(
        self,
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum Mainnet, 137 for Polygon). Specify multiple IDs as a list [1, 137] for cross-chain queries (max 5).",
        ] = None,
        contract_address: Annotated[
            str | None,
            "Contract address to filter events by (e.g., '0x1234...'). Only return events emitted by this contract.",
        ] = None,
        transaction_hash: Annotated[
            str | None,
            "Specific transaction hash to filter events by (e.g., '0xabc123...'). Useful for examining events in a particular transaction.",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. 20 results are returned per page.",
        ] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "sort_by": "block_number",
            "sort_order": "desc",
            "decode": True,
        }
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        if contract_address:
            params["filter_address"] = validate_address(contract_address)
        if transaction_hash:
            params["filter_transaction_hash"] = validate_transaction_hash(transaction_hash)
        if page:
            params["page"] = page
        out = self._get("events", params)
        out["data"] = filter_response_keys(out["data"], EVENT_KEYS_TO_KEEP)
        return out

    @tool(
        description="Retrieve events from a specific contract address. Use this to analyze activity or monitor events for a particular smart contract."
    )
    def get_contract_events(
        self,
        contract_address: Annotated[
            str,
            "The contract address to query events for (e.g., '0x1234...'). Must be a valid Ethereum address.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum Mainnet, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries (max 5).",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. 20 results are returned per page.",
        ] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "sort_by": "block_number",
            "sort_order": "desc",
            "decode": True,
        }
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        if page:
            params["page"] = page

        contract_address = validate_address(contract_address)
        return self._get(f"events/{contract_address}", params)

    @tool(
        description="Retrieve blockchain transactions with flexible filtering options. Use this to find transactions from or to an address, or between two addresses."
    )
    def get_filtered_transactions(
        self,
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries.",
        ] = None,
        from_address: Annotated[
            str | None,
            "Filter transactions sent from this address (e.g., '0x1234...'). Useful for tracking outgoing transactions from a wallet.",
        ] = None,
        to_address: Annotated[
            str | None,
            "Filter transactions sent to this address (e.g., '0x1234...'). Useful for tracking incoming transactions to a contract or wallet.",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. 20 results are returned per page.",
        ] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "sort_by": "block_number",
            "decode": True,
        }
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        if from_address:
            params["filter_from_address"] = validate_address(from_address)
        if to_address:
            params["filter_to_address"] = validate_address(to_address)
        if page:
            params["page"] = page

        out = self._get("transactions", params)
        out["data"] = filter_response_keys(out["data"], TRANSACTION_KEYS_TO_KEEP)
        return out

    @tool(
        description="Retrieve token balances for a specified address. Lists all tokens owned with their balances, metadata, and prices. The default token type is erc20."
    )
    def get_address_tokens(
        self,
        owner_address: Annotated[
            str,
            "The wallet address to get token balances for (e.g., '0x1234...'). Must be a valid Ethereum address.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries.",
        ],
        token_type: Annotated[
            Literal["erc20", "erc721", "erc1155"],
            "Type of token to query. erc20 means normal tokens, erc721 are NFTs, erc1155 are semi-fungible tokens",
        ] = "erc20",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"include_price": True, "include_spam": False}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        owner_address = validate_address(owner_address)
        return self._get(f"tokens/{token_type.lower()}/{owner_address}", params)

    @tool(
        description="Get current market prices for native and ERC20 tokens. Useful for valuation, tracking portfolio value, or monitoring price changes."
    )
    def get_token_prices(
        self,
        token_addresses: Annotated[
            list[str],
            "List of token contract addresses to get prices for (e.g., ['0x1234...', '0x5678...']). Can include ERC20 tokens. Use '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee' for native tokens (ETH, POL, MATIC, etc.).",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the tokens exist (e.g., 1 for Ethereum, 137 for Polygon). Must match the token network.",
        ] = None,
    ) -> dict[str, Any]:
        token_addresses = [validate_address(addr) for addr in token_addresses]
        params: dict[str, Any] = {"address": token_addresses}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        return self._get("tokens/price", params)

    @tool(
        description="Get metadata about a smart contract, including name, symbol, decimals, and other contract-specific information. Also returns the contract ABI which details how to interact with the contract. Use this when asked about a contract's functions, interface, or capabilities. This tool specifically retrieves details about deployed smart contracts (NOT regular wallet addresses or transaction hashes)."
    )
    def get_contract_metadata(
        self,
        contract_address: Annotated[
            str,
            "The contract address to get metadata for (e.g., '0x1234...'). Must be a deployed smart contract address (not a regular wallet). Use this for queries like 'what functions does this contract have' or 'get the ABI for contract 0x1234...'.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        contract_address = validate_address(contract_address)
        return self._get(f"contracts/metadata/{contract_address}", params)

    @tool(
        description="Retrieve detailed information about NFTs from a specific collection, including metadata, attributes, and images. Optionally get data for a specific token ID."
    )
    def get_nfts_from_contract(
        self,
        contract_address: Annotated[
            str,
            "The NFT contract address to query (e.g., '0x1234...'). Must be an ERC721 or ERC1155 contract address.",
        ],
        token_id: Annotated[
            str | None,
            "Specific token ID to query (e.g., '42'). If provided, returns data only for this NFT. Otherwise returns collection data.",
        ] = None,
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the NFT contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        params["include_metadata"] = True

        contract_address = validate_address(contract_address)
        if token_id:
            return self._get(f"nfts/{contract_address}/{token_id}", params)
        return self._get(f"nfts/{contract_address}", params)

    @tool(
        description="Get ownership information for NFTs in a specific collection. Shows which addresses own which token IDs and in what quantities."
    )
    def get_nft_owners(
        self,
        contract_address: Annotated[
            str,
            "The NFT contract address to query ownership for (e.g., '0x1234...'). Must be an ERC721 or ERC1155 contract.",
        ],
        token_id: Annotated[
            str | None,
            "Specific token ID to query owners for (e.g., '42'). If provided, shows all owners of this specific NFT.",
        ] = None,
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the NFT contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. 20 results are returned per page.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        if page:
            params["page"] = page

        contract_address = validate_address(contract_address)
        if token_id:
            return self._get(f"nfts/owners/{contract_address}/{token_id}", params)
        return self._get(f"nfts/owners/{contract_address}", params)

    @tool(
        description="Track NFT transfers for a collection, specific token, or transaction. Useful for monitoring NFT trading activity or verifying transfers."
    )
    def get_nft_transfers(
        self,
        contract_address: Annotated[
            str,
            "The NFT contract address to query transfers for (e.g., '0x1234...'). Must be an ERC721 or ERC1155 contract.",
        ],
        token_id: Annotated[
            str | None,
            "Specific token ID to query transfers for (e.g., '42'). If provided, only shows transfers of this NFT.",
        ] = None,
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). Specify the chain where the NFT contract is deployed.",
        ] = None,
        limit: Annotated[
            int | None,
            "Maximum number of transfer records to return per request. Default is 20, adjust for pagination.",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. Use with limit parameter for browsing transfer history.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

        contract_address = validate_address(contract_address)
        if token_id:
            return self._get(f"nfts/transfers/{contract_address}/{token_id}", params)
        return self._get(f"nfts/transfers/{contract_address}", params)

    @tool(
        description="Get detailed information about a specific block by its number or hash. Use this when asked about blockchain blocks (e.g., 'What's in block 12345678?' or 'Tell me about this block: 0xabc123...'). This tool is specifically for block data, NOT transactions, addresses, or contracts."
    )
    def get_block_details(
        self,
        block_identifier: Annotated[
            str,
            "Block number or block hash to look up. Can be either a simple number (e.g., '12345678') or a block hash (e.g., '0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3' for Ethereum block 0). Use for queries like 'what happened in block 14000000' or 'show me block 0xd4e56...'.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). Specify the blockchain network where the block exists.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids

        block_identifier = validate_block_identifier(block_identifier)
        out = self._get(f"resolve/{block_identifier}", params)
        return clean_resolve(out)

    @tool(
        description="Look up transactions for a wallet or contract address. Use this when asked about a specific Ethereum address (e.g., '0x1234...') to get account details including balance, transaction count, and contract verification status. This tool is specifically for addresses (accounts and contracts), NOT transaction hashes or ENS names."
    )
    def get_address_transactions(
        self,
        address: Annotated[
            str,
            "Wallet or contract address to look up (e.g., '0x1234...'). Must be a valid blockchain address starting with 0x and 42 characters long.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). Specify the blockchain network for the address.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        validated_address = validate_address(address)
        out = self._get(f"resolve/{validated_address}", params)
        return clean_resolve(out)

    @tool(
        description="Look up transactions associated with an ENS domain name (anything ending in .eth like 'vitalik.eth'). This tool is specifically for ENS domains, NOT addresses, transaction hashes, or contract queries."
    )
    def get_ens_transactions(
        self,
        ens_name: Annotated[
            str,
            "ENS name to resolve (e.g., 'vitalik.eth', 'thirdweb.eth'). Must be a valid ENS domain ending with .eth.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). ENS is primarily on Ethereum mainnet.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids
        out = self._get(f"resolve/{ens_name}", params)
        return clean_resolve(out)

    @tool(
        description="Get detailed information about a specific transaction by its hash. Use this when asked to analyze, look up, check, or get details about a transaction hash (e.g., 'What can you tell me about this transaction: 0x5407ea41...'). This tool specifically deals with transaction hashes (txid/txhash), NOT addresses, contracts, or ENS names."
    )
    def get_transaction_details(
        self,
        transaction_hash: Annotated[
            str,
            "Transaction hash to look up (e.g., '0x5407ea41de24b7353d70eab42d72c92b42a44e140f930e349973cfc7b8c9c1d7'). Must be a valid transaction hash beginning with 0x and typically 66 characters long. Use this for queries like 'tell me about this transaction' or 'what happened in transaction 0x1234...'.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). Specify the blockchain network where the transaction exists.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids

        transaction_hash = validate_transaction_hash(transaction_hash)
        out = self._get(f"resolve/{transaction_hash}", params)
        return clean_resolve(out)

    @tool(
        description="Decode a function or event signature. Use this when you need to understand what a specific function selector or event signature does and what parameters it accepts."
    )
    def decode_signature(
        self,
        signature: Annotated[
            str,
            "Function or event signature to decode (e.g., '0x095ea7b3' for the approve function). Usually begins with 0x.",
        ],
        chain_id: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). Specify to improve signature lookup accuracy.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain_ids = chain_id if chain_id is not None else self.chain_ids
        if chain_ids:
            params["chain"] = chain_ids

        signature = validate_signature(signature)
        out = self._get(f"resolve/{signature}", params)
        return clean_resolve(out)
