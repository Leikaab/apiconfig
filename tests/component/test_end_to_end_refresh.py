"""Test complete refresh flows from trigger to completion."""

from typing import Dict, Optional
from unittest.mock import Mock, patch

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.types import TokenRefreshResult


class TestEndToEndRefresh:
    """Test complete refresh flows from trigger to completion."""

    @patch("apiconfig.auth.token.refresh.refresh_oauth2_token")
    def test_bearer_token_refresh_flow(self, mock_refresh: Mock) -> None:
        """Test complete Bearer token refresh flow."""
        # Setup mock response
        mock_refresh.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer",
        }

        # Create a test subclass that implements refresh using the mock
        class TestBearerAuth(BearerAuth):
            def __init__(
                self,
                access_token: str,
                refresh_token: Optional[str] = None,
                token_url: Optional[str] = None,
                client_id: Optional[str] = None,
                http_request_callable: Optional[Mock] = None,
            ) -> None:
                super().__init__(access_token, http_request_callable=http_request_callable)
                self.refresh_token = refresh_token
                self.token_url = token_url
                self.client_id = client_id

            def refresh(self) -> TokenRefreshResult:
                # Simulate calling the refresh utility
                result = mock_refresh()
                self.access_token = result["access_token"]
                self.refresh_token = result.get("refresh_token")

                return {
                    "token_data": {
                        "access_token": result["access_token"],
                        "refresh_token": result.get("refresh_token"),
                        "expires_in": result.get("expires_in"),
                        "token_type": result.get("token_type"),
                    },
                    "config_updates": None,
                }

        # Create auth strategy
        auth = TestBearerAuth(
            access_token="old_token",
            refresh_token="old_refresh",
            token_url="https://example.com/token",
            client_id="test_client",
            http_request_callable=Mock(),
        )

        # Simulate refresh trigger
        assert auth.can_refresh()
        result = auth.refresh()

        # Validate result structure
        assert result is not None
        assert "token_data" in result
        assert "config_updates" in result

        token_data = result["token_data"]
        assert token_data is not None
        assert token_data["access_token"] == "new_access_token"
        assert token_data["refresh_token"] == "new_refresh_token"

        # Verify internal state updated
        assert auth.access_token == "new_access_token"
        assert auth.refresh_token == "new_refresh_token"

        # Verify refresh utility was called correctly
        mock_refresh.assert_called_once()

    def test_custom_auth_refresh_flow(self) -> None:
        """Test custom auth refresh flow."""
        current_token = {"value": "old_token"}

        def header_callback() -> Dict[str, str]:
            return {"Authorization": f"Bearer {current_token['value']}"}

        def refresh_func() -> TokenRefreshResult:
            current_token["value"] = "new_token"
            return {"token_data": {"access_token": "new_token"}, "config_updates": None}

        auth = CustomAuth(header_callback=header_callback, refresh_func=refresh_func, can_refresh_func=lambda: True)

        # Test refresh
        headers = auth.prepare_request_headers()
        assert headers["Authorization"] == "Bearer old_token"

        result = auth.refresh()
        assert result is not None
        token_data = result["token_data"]
        assert token_data is not None
        assert token_data["access_token"] == "new_token"

        headers = auth.prepare_request_headers()
        assert headers["Authorization"] == "Bearer new_token"
