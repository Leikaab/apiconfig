"""Test integration with existing apiconfig components."""

import logging
from io import StringIO
from typing import Any, Dict
from unittest.mock import Mock as MockClass

from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.auth.token.storage import InMemoryTokenStorage
from apiconfig.types import TokenRefreshResult


class TestExistingComponentIntegration:
    """Test integration with existing apiconfig components."""

    def test_token_storage_integration(self) -> None:
        """Test integration with TokenStorage."""
        storage = InMemoryTokenStorage()

        # Store initial token data
        storage.store_token("test_key", {"access_token": "stored_token", "refresh_token": "stored_refresh", "expires_at": "2024-12-31T23:59:59Z"})

        # Simulate loading from storage and creating auth strategy
        stored_data = storage.retrieve_token("test_key")
        assert stored_data is not None
        auth = BearerAuth(access_token=stored_data["access_token"])

        # Note: BearerAuth doesn't have refresh_token or expires_at attributes
        # In a real implementation, these would be handled by the application layer
        assert auth.access_token == "stored_token"

        # Create a test subclass that implements refresh
        class TestBearerAuth(BearerAuth):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                self.refresh_token: str = "default_refresh"
                self.expires_at: str = "default_expires"

            def refresh(self) -> TokenRefreshResult:
                # Simulate refresh
                self.access_token = "new_token"
                self.refresh_token = "new_refresh"
                return {"token_data": {"access_token": "new_token", "refresh_token": "new_refresh"}, "config_updates": None}

        # Test saving back to storage after refresh
        mock_http = MockClass()
        mock_http.return_value = MockClass(json=lambda: {"access_token": "new_token", "refresh_token": "new_refresh"})

        auth = TestBearerAuth(access_token="stored_token", http_request_callable=mock_http)
        auth.refresh_token = "stored_refresh"

        result = auth.refresh()

        # Simulate saving updated token data back to storage
        assert result is not None
        token_data = result.get("token_data")
        assert token_data is not None
        updated_token_data = {
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": "2024-12-31T23:59:59Z",  # Would be calculated from expires_in
        }
        storage.store_token("test_key", updated_token_data)

        updated_data = storage.retrieve_token("test_key")
        assert updated_data is not None
        assert updated_data["access_token"] == "new_token"

    def test_logging_integration(self) -> None:
        """Test integration with logging system."""
        # Capture log output
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        logger = logging.getLogger("apiconfig")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        try:
            mock_http = MockClass()
            mock_http.return_value = MockClass(json=lambda: {"access_token": "new_token"})

            # Create a test subclass that logs during refresh
            class TestBearerAuth(BearerAuth):
                def refresh(self) -> TokenRefreshResult:
                    logger.info("Bearer token refresh started")
                    self.access_token = "new_token"
                    logger.info("Bearer token refresh successful")
                    return {"token_data": {"access_token": "new_token"}, "config_updates": None}

            auth = TestBearerAuth(access_token="old_token", http_request_callable=mock_http)

            auth.refresh()

            log_output = log_capture.getvalue()
            assert "Bearer token refresh" in log_output
            assert "refresh successful" in log_output.lower()

        finally:
            logger.removeHandler(handler)

    def test_custom_auth_storage_integration(self) -> None:
        """Test custom auth integration with token storage."""
        storage = InMemoryTokenStorage()

        # Store initial custom token data
        storage.store_token("custom_key", {"api_key": "stored_api_key", "session_token": "stored_session"})

        stored_data = storage.retrieve_token("custom_key")
        assert stored_data is not None
        current_token = {"value": stored_data["api_key"]}

        def header_callback() -> Dict[str, str]:
            return {"X-API-Key": current_token["value"]}

        def refresh_func() -> TokenRefreshResult:
            # Simulate refresh
            new_key = "refreshed_api_key"
            current_token["value"] = new_key

            # Update storage
            assert stored_data is not None
            updated_data = stored_data.copy()
            updated_data["api_key"] = new_key
            storage.store_token("custom_key", updated_data)

            return {"token_data": {"access_token": new_key}, "config_updates": None}

        auth = CustomAuth(header_callback=header_callback, refresh_func=refresh_func, can_refresh_func=lambda: True)

        # Test initial state
        headers = auth.prepare_request_headers()
        assert headers["X-API-Key"] == "stored_api_key"

        # Test refresh and storage update
        result = auth.refresh()
        assert result is not None
        token_data = result.get("token_data")
        assert token_data is not None
        assert token_data.get("access_token") == "refreshed_api_key"

        # Verify storage was updated
        updated_data = storage.retrieve_token("custom_key")
        assert updated_data is not None
        assert updated_data["api_key"] == "refreshed_api_key"

        # Verify auth uses new token
        headers = auth.prepare_request_headers()
        assert headers["X-API-Key"] == "refreshed_api_key"
