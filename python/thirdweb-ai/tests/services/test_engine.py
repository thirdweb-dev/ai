import os

import pytest

from thirdweb_ai.services.engine import Engine


class MockEngine(Engine):
    def __init__(
        self,
        engine_url: str,
        engine_auth_jwt: str,
        chain_id: int | str | None = None,
        backend_wallet_address: str | None = None,
        secret_key: str = "",
    ):
        super().__init__(
            engine_url=engine_url,
            engine_auth_jwt=engine_auth_jwt,
            chain_id=chain_id,
            backend_wallet_address=backend_wallet_address,
            secret_key=secret_key,
        )


@pytest.fixture
def engine():
    return MockEngine(
        engine_url="https://engine.thirdweb-dev.com",
        engine_auth_jwt="test_jwt",
        chain_id=84532,
        backend_wallet_address="0xC22166664e820cdA6bf4cedBdbb4fa1E6A84C440",
        secret_key=os.getenv("__THIRDWEB_SECRET_KEY_DEV") or "",
    )


class TestEngine:
    # Constants
    CHAIN_ID = "84532"
    TEST_ADDRESS = "0xC22166664e820cdA6bf4cedBdbb4fa1E6A84C440"
    TEST_QUEUE_ID = "9eb88b00-f04f-409b-9df7-7dcc9003bc35"

    # def test_create_backend_wallet(self, engine: Engine):
    #     create_backend_wallet = engine.create_backend_wallet.__wrapped__
    #     result = create_backend_wallet(engine, wallet_type="local", label="Test Wallet")
    #
    #     assert isinstance(result, dict)
