import os

import pytest

from thirdweb_ai.services.nebula import Nebula


class MockNebula(Nebula):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.base_url = "https://nebula.thirdweb-dev.com"


@pytest.fixture
def nebula():
    return MockNebula(secret_key=os.getenv("__THIRDWEB_SECRET_KEY_DEV") or "")


class TestNebula:
    # Test constants
    TEST_MESSAGE = "What is thirdweb?"
    TEST_SESSION_ID = "test-session-id"
    TEST_CONTEXT = {"chainIds": ["1", "137"], "walletAddress": "0x123456789abcdef"}

    def test_chat(self, nebula: Nebula):
        chat = nebula.chat.__wrapped__
        result = chat(nebula, message=self.TEST_MESSAGE, session_id=self.TEST_SESSION_ID, context=self.TEST_CONTEXT)

        assert isinstance(result, dict)

    def test_list_sessions(self, nebula: Nebula):
        list_sessions = nebula.list_sessions.__wrapped__
        result = list_sessions(nebula)

        assert isinstance(result, dict)

    def test_get_session(self, nebula: Nebula):
        get_session = nebula.get_session.__wrapped__
        result = get_session(nebula, session_id=self.TEST_SESSION_ID)

        assert isinstance(result, dict)

