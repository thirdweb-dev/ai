from typing import Annotated, Any

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class Insight(Service):
    def __init__(self, secret_key: str, chain_id: int | list[int]):
        super().__init__(base_url="https://insight.thirdweb.com/v1", secret_key=secret_key)
        self.chain_ids = chain_id if isinstance(chain_id, list) else [chain_id]

    @tool(
        description="Retrieve blockchain events with flexible filtering options. Use this to search for specific events or to analyze event patterns across multiple blocks."
    )
    def get_events(
        self,
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum Mainnet, 137 for Polygon). Specify multiple IDs as a list [1, 137] for cross-chain queries (max 5).",
        ] = None,
        address: Annotated[
            str | None,
            "Contract address to filter events by (e.g., '0x1234...'). Only return events emitted by this contract.",
        ] = None,
        decode: Annotated[
            bool | None, "Set to True to decode event data into human-readable format using contract ABIs."
        ] = None,
        block_number: Annotated[int | None, "Exact block number to query events from (e.g., 15000000)."] = None,
        block_number_gte: Annotated[int | None, "Minimum block number to start querying from (inclusive)."] = None,
        block_number_lt: Annotated[int | None, "Maximum block number to query up to (exclusive)."] = None,
        transaction_hash: Annotated[
            str | None,
            "Specific transaction hash to filter events by (e.g., '0xabc123...'). Useful for examining events in a particular transaction.",
        ] = None,
        topic_0: Annotated[
            str | None,
            "Filter by event signature hash (first topic). For example, '0xa6697e974e6a320f454390be03f74955e8978f1a6971ea6730542e37b66179bc' for Transfer events.",
        ] = None,
        limit: Annotated[
            int | None, "Maximum number of events to return per request. Default is 20, adjust for pagination."
        ] = None,
        page: Annotated[
            int | None, "Page number for paginated results, starting from 0. Use with limit parameter."
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if address:
            params["filter_address"] = address
        if decode:
            params["decode"] = decode
        if block_number:
            params["filter_block_number"] = block_number
        if block_number_gte:
            params["filter_block_number_gte"] = block_number_gte
        if block_number_lt:
            params["filter_block_number_lt"] = block_number_lt
        if transaction_hash:
            params["filter_transaction_hash"] = transaction_hash
        if topic_0:
            params["filter_topic_0"] = topic_0
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        return self._get("events", params)

    @tool(
        description="Retrieve events from a specific contract address. Use this to analyze activity or monitor events for a particular smart contract."
    )
    def get_contract_events(
        self,
        contract_address: Annotated[
            str, "The contract address to query events for (e.g., '0x1234...'). Must be a valid Ethereum address."
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum Mainnet, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries (max 5).",
        ] = None,
        decode: Annotated[
            bool | None, "Set to True to decode event data into human-readable format using the contract's ABI."
        ] = None,
        block_number_gte: Annotated[
            int | None,
            "Only return events from blocks with number greater than or equal to this value. Useful for querying recent history.",
        ] = None,
        topic_0: Annotated[
            str | None,
            "Filter by event signature hash (first topic). For example, Transfer event has a specific signature hash.",
        ] = None,
        limit: Annotated[
            int | None, "Maximum number of events to return per request. Default is 20, increase for more results."
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. Use with limit parameter for browsing large result sets.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if decode:
            params["decode"] = decode
        if block_number_gte:
            params["filter_block_number_gte"] = block_number_gte
        if topic_0:
            params["filter_topic_0"] = topic_0
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        return self._get(f"events/{contract_address}", params)

    @tool(
        description="Get events for a specific contract filtered by event signature. Useful for tracking particular event types like Transfers, Approvals, or custom events."
    )
    def get_contract_events_by_signature(
        self,
        contract_address: Annotated[
            str, "The contract address to query events for (e.g., '0x1234...'). Must be a valid Ethereum address."
        ],
        signature: Annotated[
            str,
            "Event signature to filter by (e.g., 'Transfer(address,address,uint256)' or the hash '0xddf252ad...'). This determines which type of events to retrieve.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries.",
        ] = None,
        decode: Annotated[
            bool | None,
            "Set to True to decode event data into human-readable format. Recommended for easier interpretation.",
        ] = None,
        block_number_gte: Annotated[
            int | None,
            "Only return events from blocks with number greater than or equal to this value. Useful for recent history.",
        ] = None,
        limit: Annotated[
            int | None, "Maximum number of events to return per request. Default is 20, adjust based on your needs."
        ] = None,
        page: Annotated[
            int | None, "Page number for paginated results, starting from 0. Use for browsing large result sets."
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if decode:
            params["decode"] = decode
        if block_number_gte:
            params["filter_block_number_gte"] = block_number_gte
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        return self._get(f"events/{contract_address}/{signature}", params)

    @tool(
        description="Retrieve blockchain transactions with flexible filtering options. Use this to analyze transaction patterns, track specific transactions, or monitor wallet activity."
    )
    def get_all_transactions(
        self,
        chain: Annotated[
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
        function_selector: Annotated[
            str | None,
            "Filter by function selector (e.g., '0x095ea7b3' for the approve function). Useful for finding specific contract interactions.",
        ] = None,
        decode: Annotated[
            bool,
            "Set to True to decode transaction input data using contract ABIs. Makes contract interactions human-readable.",
        ] = True,
        sort_order: Annotated[
            str | None,
            "Sort order for the transactions. Default is 'asc' for ascending order. Use 'desc' for descending order.",
        ] = "desc",
        limit: Annotated[
            int | None,
            "Maximum number of transactions to return per request. Default is 20, adjust based on your needs.",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. Use with limit parameter for browsing large result sets.",
        ] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "sort_by": "block_timestamp",
            "sort_order": sort_order if sort_order in ["asc", "desc"] else "desc",
        }
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if from_address:
            params["filter_from_address"] = from_address
        if to_address:
            params["filter_to_address"] = to_address
        if function_selector:
            params["filter_function_selector"] = function_selector
        if decode:
            params["decode"] = decode
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        return self._get("transactions", params)

    @tool(
        description="Retrieve ERC20 token balances for a specified address. Lists all fungible tokens owned with their balances, metadata, and optionally prices."
    )
    def get_erc20_tokens(
        self,
        owner_address: Annotated[
            str,
            "The wallet address to get ERC20 token balances for (e.g., '0x1234...'). Must be a valid Ethereum address.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries.",
        ] = None,
        include_price: Annotated[
            bool | None,
            "Set to True to include current market prices for tokens. Useful for calculating portfolio value.",
        ] = None,
        include_spam: Annotated[
            bool | None,
            "Set to True to include suspected spam tokens. Default is False to filter out unwanted tokens.",
        ] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if include_price:
            params["include_price"] = include_price
        if include_spam:
            params["include_spam"] = include_spam
        return self._get(f"tokens/erc20/{owner_address}", params)

    @tool(
        description="Retrieve ERC721 NFTs (non-fungible tokens) owned by a specified address. Lists all unique NFTs with their metadata and optionally prices."
    )
    def get_erc721_tokens(
        self,
        owner_address: Annotated[
            str,
            "The wallet address to get ERC721 NFTs for (e.g., '0x1234...'). Returns all NFTs owned by this address.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries.",
        ] = None,
        include_price: Annotated[
            bool | None, "Set to True to include estimated prices for NFTs where available. Useful for valuation."
        ] = None,
        include_spam: Annotated[
            bool | None,
            "Set to True to include suspected spam NFTs. Default is False to filter out potentially unwanted items.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if include_price:
            params["include_price"] = include_price
        if include_spam:
            params["include_spam"] = include_spam
        return self._get(f"tokens/erc721/{owner_address}", params)

    @tool(
        description="Retrieve ERC1155 tokens (semi-fungible tokens) owned by a specified address. Shows balances of multi-token contracts with metadata."
    )
    def get_erc1155_tokens(
        self,
        owner_address: Annotated[
            str,
            "The wallet address to get ERC1155 tokens for (e.g., '0x1234...'). Returns all token IDs and their quantities.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum, 137 for Polygon). Specify multiple IDs as a list for cross-chain queries.",
        ] = None,
        include_price: Annotated[
            bool | None, "Set to True to include estimated prices for tokens where available. Useful for valuation."
        ] = None,
        include_spam: Annotated[
            bool | None,
            "Set to True to include suspected spam tokens. Default is False to filter out potentially unwanted items.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if include_price:
            params["include_price"] = include_price
        if include_spam:
            params["include_spam"] = include_spam
        return self._get(f"tokens/erc1155/{owner_address}", params)

    @tool(
        description="Get current market prices for specified tokens. Useful for valuation, tracking portfolio value, or monitoring price changes."
    )
    def get_token_prices(
        self,
        token_addresses: Annotated[
            list[str],
            "List of token contract addresses to get prices for (e.g., ['0x1234...', '0x5678...']). Can include ERC20 tokens.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the tokens exist (e.g., 1 for Ethereum, 137 for Polygon). Must match the token network.",
        ] = None,
        currencies: Annotated[
            list[str] | None,
            "List of currencies to return prices in (e.g., ['usd', 'eth']). Default is USD if not specified.",
        ] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"token_addresses": token_addresses}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if currencies:
            params["currencies"] = currencies
        return self._get("tokens/price", params)

    @tool(
        description="Retrieve the Application Binary Interface (ABI) for a smart contract. Essential for decoding contract data and interacting with the contract."
    )
    def get_contract_abi(
        self,
        contract_address: Annotated[
            str,
            "The contract address to get the ABI for (e.g., '0x1234...'). Must be a deployed and verified contract.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        return self._get(f"contracts/abi/{contract_address}", params)

    @tool(
        description="Get metadata about a smart contract, including name, symbol, decimals, and other contract-specific information."
    )
    def get_contract_metadata(
        self,
        contract_address: Annotated[
            str,
            "The contract address to get metadata for (e.g., '0x1234...'). Works for tokens and other contract types.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        return self._get(f"contracts/metadata/{contract_address}", params)

    @tool(
        description="Retrieve detailed information about NFTs from a specific collection, including metadata, attributes, and images. Optionally get data for a specific token ID."
    )
    def get_nfts(
        self,
        contract_address: Annotated[
            str, "The NFT contract address to query (e.g., '0x1234...'). Must be an ERC721 or ERC1155 contract."
        ],
        token_id: Annotated[
            str | None,
            "Specific token ID to query (e.g., '42'). If provided, returns data only for this NFT. Otherwise returns collection data.",
        ] = None,
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the NFT contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
        include_metadata: Annotated[
            bool | None,
            "Set to True to include full NFT metadata like attributes, image URL, etc. Useful for displaying NFT details.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if include_metadata:
            params["include_metadata"] = include_metadata

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
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) where the NFT contract is deployed (e.g., 1 for Ethereum). Specify the correct network.",
        ] = None,
        limit: Annotated[
            int | None,
            "Maximum number of ownership records to return per request. Default is 20, adjust for pagination.",
        ] = None,
        page: Annotated[
            int | None,
            "Page number for paginated results, starting from 0. Use with limit parameter for browsing large collections.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

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
        chain: Annotated[
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
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

        if token_id:
            return self._get(f"nfts/transfers/{contract_address}/{token_id}", params)
        return self._get(f"nfts/transfers/{contract_address}", params)

    @tool(
        description="Resolve ENS names to Ethereum addresses or vice versa. Useful for working with human-readable names instead of addresses."
    )
    def resolve(
        self,
        input_data: Annotated[
            str,
            "The ENS name (e.g., 'thirdweb.eth') or address (e.g., '0x1234...') to resolve. Works in both directions.",
        ],
        chain: Annotated[
            list[int] | int | None,
            "Chain ID(s) to query (e.g., 1 for Ethereum). ENS is primarily on Ethereum mainnet.",
        ] = None,
    ) -> dict[str, Any]:
        params = {}
        chain = chain or self.chain_ids
        if chain:
            params["chain"] = chain
        return self._get(f"resolve/{input_data}", params)
