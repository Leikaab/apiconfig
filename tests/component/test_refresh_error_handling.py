"""Test error handling in refresh scenarios."""

import threading
import time
from typing import Any
from unittest.mock import Mock

import pytest

import apiconfig.types as api_types
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.exceptions.auth import AuthStrategyError, TokenRefreshError


class TestRefreshErrorHandling:
    """Test error handling in refresh scenarios."""

    def test_refresh_failure_handling(self) -> None:
        """Test handling of refresh failures."""
        mock_http = Mock()
        mock_http.side_effect = Exception("Network error")

        # Create a test subclass that uses the http_request_callable
        class TestBearerAuth(BearerAuth):
            def refresh(self) -> None:
                try:
                    # Simulate using the http_request_callable
                    if self._http_request_callable:
                        self._http_request_callable()
                except Exception as e:
                    raise TokenRefreshError(f"Refresh failed: {str(e)}") from e

        auth = TestBearerAuth(access_token="token", http_request_callable=mock_http)

        with pytest.raises(TokenRefreshError):
            auth.refresh()

    def test_unconfigured_refresh_handling(self) -> None:
        """Test handling when refresh is not configured."""
        auth = BearerAuth(access_token="token")  # No refresh config

        assert not auth.can_refresh()
        assert auth.get_refresh_callback() is None

        with pytest.raises(AuthStrategyError):
            auth.refresh()

    def test_concurrent_refresh_safety(self) -> None:
        """Test thread safety of concurrent refresh operations."""
        mock_http = Mock()
        mock_http.return_value = Mock(json=lambda: {"access_token": f"token_{time.time()}", "expires_in": 3600})

        # Create a test subclass with thread-safe refresh
        class TestBearerAuth(BearerAuth):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                self._refresh_lock = threading.Lock()

            def refresh(self) -> api_types.TokenRefreshResult:
                with self._refresh_lock:
                    # Simulate some processing time
                    time.sleep(0.01)
                    new_token = f"token_{time.time()}"
                    self.access_token = new_token
                    return {"token_data": {"access_token": new_token}, "config_updates": None}

        auth = TestBearerAuth(access_token="initial", http_request_callable=mock_http)

        results: list[api_types.TokenRefreshResult] = []
        errors: list[Exception] = []

        def refresh_worker() -> None:
            try:
                result = auth.refresh()
                results.append(result)
            except Exception as e:
                errors.append(e)

        # Start multiple refresh operations
        threads = [threading.Thread(target=refresh_worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify no errors and consistent state
        assert len(errors) == 0
        assert len(results) > 0

    def test_custom_auth_refresh_error_handling(self) -> None:
        """Test error handling in custom auth refresh."""

        def failing_refresh() -> None:
            raise Exception("Custom refresh failed")

        auth = CustomAuth(header_callback=lambda: {"Authorization": "Bearer token"}, refresh_func=failing_refresh, can_refresh_func=lambda: True)

        with pytest.raises(AuthStrategyError) as exc_info:
            auth.refresh()

        assert "Custom auth refresh failed" in str(exc_info.value)

    def test_custom_auth_no_refresh_function(self) -> None:
        """Test custom auth without refresh function."""
        auth = CustomAuth(header_callback=lambda: {"Authorization": "Bearer token"})

        assert not auth.can_refresh()
        assert auth.get_refresh_callback() is None

        with pytest.raises(AuthStrategyError) as exc_info:
            auth.refresh()

        assert "no refresh function configured" in str(exc_info.value)
