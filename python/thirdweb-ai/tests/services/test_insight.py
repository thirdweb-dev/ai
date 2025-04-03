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

    def test_get_erc20_tokens(self, insight: Insight):
        get_erc20_tokens = insight.get_erc20_tokens.__wrapped__
        result = get_erc20_tokens(insight, chain=self.CHAIN_ID, owner_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)
        assert "data" in result
