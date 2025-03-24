import pytest
from unittest.mock import MagicMock, patch

from thirdweb_ai.services.engine import Engine
from thirdweb_ai.common.utils import extract_digits


class TestEngine:
    @pytest.fixture
    def engine(self):
        """Create an Engine instance for testing"""
        return Engine(
            engine_url="https://api.thirdweb.com/v1",
            engine_auth_jwt="test_jwt",
            chain_id="1",
            backend_wallet_address="0x1234567890123456789012345678901234567890",
            secret_key="test_secret",
        )

    @pytest.mark.parametrize(
        "value,expected_hex",
        [
            ("1000000000000000000", "0x" + hex(1000000000000000000)[2:]),  # 1 ETH
            ("0", "0x0"),  # Zero value
            ("500", "0x1f4"),  # Small value
            ("ethereum-1", "0x1"),  # Text with number
        ],
    )
    def test_send_transaction_value_conversion(self, engine, value, expected_hex):
        """Test that value is properly converted to hex in send_transaction"""
        with patch.object(engine, "_post") as mock_post:
            mock_post.return_value = {"success": True}
            
            # Call the send_transaction method with the correct parameter names
            result = engine.send_transaction(
                to_address="0x2222222222222222222222222222222222222222",
                value=value,
                data="0x",
                chain_id="1",
            )
            
            # Verify the POST request was made with the correct payload
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            assert args[0] == "backend-wallet/1/send-transaction"
            assert kwargs["data"]["toAddress"] == "0x2222222222222222222222222222222222222222"
            assert kwargs["data"]["value"] == expected_hex
            assert kwargs["data"]["data"] == "0x"
            assert kwargs["headers"]["X-Backend-Wallet-Address"] == "0x1234567890123456789012345678901234567890"
            
            assert result == {"success": True}

    def test_send_transaction_error_handling(self, engine):
        """Test that errors in value conversion are properly handled"""
        with pytest.raises(ValueError, match="does not contain any digits"):
            engine.send_transaction(
                to_address="0x2222222222222222222222222222222222222222",
                value="no-digits-here",
                data="0x",
                chain_id="1",
            )

    def test_send_transaction_integration(self, engine):
        """Test the full API request flow with mocked httpx client"""
        with patch("httpx.Client") as mock_client:
            # Set up the mock client and response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "queueId": "123456",
                "hash": "0xabcdef",
                "status": "submitted"
            }
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = MagicMock()
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance
            
            # Create engine with custom client
            test_engine = Engine(
                engine_url="https://api.thirdweb.com/v1",
                engine_auth_jwt="test_jwt",
                chain_id="1",
                backend_wallet_address="0x1234567890123456789012345678901234567890",
                secret_key="test_secret",
            )
            # Replace the client
            test_engine.client = mock_client_instance
            
            # Call send_transaction
            result = test_engine.send_transaction(
                to_address="0x2222222222222222222222222222222222222222",
                value="1000000000000000000",
                data="0x",
                chain_id="1",
            )
            
            # Verify the result
            assert result == {
                "queueId": "123456",
                "hash": "0xabcdef",
                "status": "submitted"
            }
            
            # Verify the request was made correctly
            expected_url = "https://api.thirdweb.com/v1/backend-wallet/1/send-transaction"
            expected_headers = {
                "Content-Type": "application/json",
                "X-Secret-Key": "test_secret",
                "Authorization": "Bearer test_jwt",
                "X-Backend-Wallet-Address": "0x1234567890123456789012345678901234567890"
            }
            expected_json = {
                "toAddress": "0x2222222222222222222222222222222222222222",
                "value": "0xde0b6b3a7640000",  # hex for 1000000000000000000
                "data": "0x"
            }
            
            mock_client_instance.post.assert_called_once_with(
                expected_url,
                json=expected_json,
                headers=expected_headers
            )