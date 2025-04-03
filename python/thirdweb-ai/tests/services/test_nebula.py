import os
import typing

import pytest

from thirdweb_ai.services.nebula import Nebula


class MockNebula(Nebula):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.base_url = "https://nebula-api.thirdweb-dev.com"


@pytest.fixture
def nebula():
    return MockNebula(secret_key=os.getenv("__THIRDWEB_SECRET_KEY_DEV") or "")


class TestNebula:
    TEST_MESSAGE = "What is thirdweb?"
    TEST_SESSION_ID = "test-session-id"
    TEST_CONTEXT: typing.ClassVar = {"chainIds": ["1", "137"], "walletAddress": "0x123456789abcdef"}

    def test_chat(self, nebula: Nebula):
        chat = nebula.chat.__wrapped__
        result = chat(nebula, message=self.TEST_MESSAGE, session_id=self.TEST_SESSION_ID, context=self.TEST_CONTEXT)

        assert isinstance(result, dict)
