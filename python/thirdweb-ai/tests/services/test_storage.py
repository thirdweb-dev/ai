import os
from typing import ClassVar
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from thirdweb_ai.services.storage import Storage


class MockStorage(Storage):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.base_url = "https://storage.thirdweb.com"


@pytest.fixture
def storage():
    return MockStorage(secret_key=os.getenv("__THIRDWEB_SECRET_KEY_DEV") or "test-key")


class TestStorage:
    # Constants
    TEST_IPFS_HASH: ClassVar[str] = "ipfs://QmTcHZQ5QEjjbBMJrz7Xaz9AQyVBqsKCS4YQQ71B3gDQ4f"
    TEST_CONTENT: ClassVar[dict[str, str]] = {"name": "test", "description": "test description"}

    def test_fetch_ipfs_content(self, storage: Storage):
        fetch_ipfs_content = storage.fetch_ipfs_content.__wrapped__

        # Test invalid IPFS hash
        result = fetch_ipfs_content(storage, ipfs_hash="invalid-hash")
        assert "error" in result

        # Mock the _get method to return test content
        storage._get = MagicMock(return_value=self.TEST_CONTENT)  # type:ignore[assignment] # noqa: SLF001

        # Test valid IPFS hash
        result = fetch_ipfs_content(storage, ipfs_hash=self.TEST_IPFS_HASH)
        assert result == self.TEST_CONTENT
        storage._get.assert_called_once()  # noqa: SLF001 # type:ignore[union-attr]

    @pytest.mark.asyncio
    async def test_upload_to_ipfs_json(self, storage: Storage):
        upload_to_ipfs = storage.upload_to_ipfs.__wrapped__

        # Create test data
        class TestModel(BaseModel):
            name: str
            value: int

        test_model = TestModel(name="test", value=123)

        # Mock the _async_post_file method
        with patch.object(storage, "_async_post_file", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = {"IpfsHash": "QmTest123"}

            # Test with dict
            result = await upload_to_ipfs(storage, data={"test": "value"})
            assert result == "ipfs://QmTest123"

            # Test with Pydantic model
            result = await upload_to_ipfs(storage, data=test_model)
            assert result == "ipfs://QmTest123"

            # Verify post was called
            assert mock_post.call_count == 2

