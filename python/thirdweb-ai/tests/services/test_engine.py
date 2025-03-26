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

    def test_create_backend_wallet(self, engine: Engine):
        create_backend_wallet = engine.create_backend_wallet.__wrapped__
        result = create_backend_wallet(engine, wallet_type="local", label="Test Wallet")

        assert isinstance(result, dict)

    def test_get_all_backend_wallet(self, engine: Engine):
        get_all_backend_wallet = engine.get_all_backend_wallet.__wrapped__
        result = get_all_backend_wallet(engine, page=1, limit=10)

        assert isinstance(result, dict)

    def test_get_wallet_balance(self, engine: Engine):
        get_wallet_balance = engine.get_wallet_balance.__wrapped__
        result = get_wallet_balance(engine, chain_id=self.CHAIN_ID, backend_wallet_address=self.TEST_ADDRESS)

        assert isinstance(result, dict)

    def test_send_transaction(self, engine: Engine):
        send_transaction = engine.send_transaction.__wrapped__
        result = send_transaction(
            engine,
            to_address=self.TEST_ADDRESS,
            value="0",
            data="0x",
            chain_id=self.CHAIN_ID,
            backend_wallet_address=self.TEST_ADDRESS,
        )

        assert isinstance(result, dict)

    def test_get_transaction_status(self, engine: Engine):
        get_transaction_status = engine.get_transaction_status.__wrapped__
        result = get_transaction_status(engine, queue_id=self.TEST_QUEUE_ID)

        assert isinstance(result, dict)

    def test_read_contract(self, engine: Engine):
        read_contract = engine.read_contract.__wrapped__
        result = read_contract(
            engine,
            contract_address=self.TEST_ADDRESS,
            function_name="balanceOf",
            function_args=[self.TEST_ADDRESS],
            chain_id=self.CHAIN_ID,
        )

        assert isinstance(result, dict)

    def test_write_contract(self, engine: Engine):
        write_contract = engine.write_contract.__wrapped__
        result = write_contract(
            engine,
            contract_address=self.TEST_ADDRESS,
            function_name="transfer",
            function_args=[self.TEST_ADDRESS, "1000000000000000000"],
            value="0",
            chain_id=self.CHAIN_ID,
        )

        assert isinstance(result, dict)

