import os

import pytest

from thirdweb_ai.services.insight import Insight


class MockInsight(Insight):
    def __init__(self, secret_key: str, chain_id: int | str | list[int | str]):
        super().__init__(secret_key=secret_key, chain_id=chain_id)
        self.base_url = "https://insight.thirdweb-dev.com/v1"


@pytest.fixture
def insight():
    return MockInsight(secret_key=os.getenv("__THIRDWEB_SECRET_KEY_DEV") or "", chain_id=84532)


class TestInsight:
    # Constants
    CHAIN_ID = 1
    TEST_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    TEST_DOMAIN = "thirdweb.eth"
    DEFAULT_LIMIT = 5

    def test_get_all_events(self, insight: Insight):
        get_all_events = insight.get_all_events.__wrapped__
        result = get_all_events(insight, chain=self.CHAIN_ID, address=self.TEST_ADDRESS, limit=self.DEFAULT_LIMIT)

        assert isinstance(result, dict)
        assert "meta" in result

    def test_get_contract_events(self, insight: Insight):
        get_contract_events = insight.get_contract_events.__wrapped__
        result = get_contract_events(
            insight, chain=self.CHAIN_ID, contract_address=self.TEST_ADDRESS, limit=self.DEFAULT_LIMIT
        )

        assert isinstance(result, dict)
        assert "meta" in result

    def test_get_all_transactions(self, insight: Insight):
        get_all_transactions = insight.get_all_transactions.__wrapped__
        result = get_all_transactions(insight, chain=self.CHAIN_ID, limit=self.DEFAULT_LIMIT)

        assert isinstance(result, dict)
        assert "meta" in result

    def test_get_erc20_tokens(self, insight: Insight):
        get_erc20_tokens = insight.get_erc20_tokens.__wrapped__
        result = get_erc20_tokens(insight, chain=self.CHAIN_ID, owner_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_erc721_tokens(self, insight: Insight):
        get_erc721_tokens = insight.get_erc721_tokens.__wrapped__
        result = get_erc721_tokens(insight, chain=self.CHAIN_ID, owner_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_erc1155_tokens(self, insight: Insight):
        get_erc1155_tokens = insight.get_erc1155_tokens.__wrapped__
        result = get_erc1155_tokens(insight, chain=self.CHAIN_ID, owner_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_token_prices(self, insight: Insight):
        get_token_prices = insight.get_token_prices.__wrapped__
        result = get_token_prices(insight, chain=self.CHAIN_ID, token_addresses=[self.TEST_ADDRESS])

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_contract_metadata(self, insight: Insight):
        get_contract_metadata = insight.get_contract_metadata.__wrapped__
        result = get_contract_metadata(insight, chain=self.CHAIN_ID, contract_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_nfts(self, insight: Insight):
        get_nfts = insight.get_nfts.__wrapped__
        result = get_nfts(insight, chain=self.CHAIN_ID, contract_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_nft_owners(self, insight: Insight):
        get_nft_owners = insight.get_nft_owners.__wrapped__
        result = get_nft_owners(insight, chain=self.CHAIN_ID, contract_address=self.TEST_ADDRESS, limit=self.DEFAULT_LIMIT)

        assert isinstance(result, dict)
        assert "data" in result

    def test_get_nft_transfers(self, insight: Insight):
        get_nft_transfers = insight.get_nft_transfers.__wrapped__
        result = get_nft_transfers(
            insight, chain=self.CHAIN_ID, contract_address=self.TEST_ADDRESS, limit=self.DEFAULT_LIMIT
        )

        assert isinstance(result, dict)
        assert "data" in result

    def test_resolve(self, insight: Insight):
        resolve = insight.resolve.__wrapped__
        result = resolve(insight, chain=self.CHAIN_ID, input_data=self.TEST_DOMAIN)

        assert isinstance(result, dict)
        assert "data" in result
