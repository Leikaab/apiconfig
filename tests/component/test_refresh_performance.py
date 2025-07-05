"""Test performance characteristics of refresh operations."""

import time
from typing import Any, Dict
from unittest.mock import Mock

import apiconfig.types as api_types
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth


class TestRefreshPerformance:
    """Test performance characteristics of refresh operations."""

    def test_refresh_performance(self) -> None:
        """Test refresh operation performance."""
        mock_http = Mock()
        mock_http.return_value = Mock(json=lambda: {"access_token": "new_token", "expires_in": 3600})

        # Create a test subclass that implements refresh
        class TestBearerAuth(BearerAuth):
            def refresh(self) -> api_types.TokenRefreshResult:
                # Simulate minimal refresh logic
                self.access_token = "new_token"
                return {"token_data": {"access_token": "new_token"}, "config_updates": None}

        auth = TestBearerAuth(access_token="token", http_request_callable=mock_http)

        # Measure refresh time
        start_time = time.time()
        auth.refresh()
        refresh_time = time.time() - start_time

        # Should complete quickly (< 100ms excluding network)
        assert refresh_time < 0.1

    def test_callback_overhead(self) -> None:
        """Test overhead of refresh callback mechanism."""
        auth = BearerAuth(access_token="token")

        # Measure callback creation time
        start_time = time.time()
        auth.get_refresh_callback()  # Test callback creation overhead
        callback_time = time.time() - start_time

        # Should be negligible overhead
        assert callback_time < 0.01

    def test_custom_auth_performance(self) -> None:
        """Test custom auth performance characteristics."""
        call_count = 0

        def header_callback() -> Dict[str, str]:
            nonlocal call_count
            call_count += 1
            return {"Authorization": f"Bearer token_{call_count}"}

        def refresh_func() -> api_types.TokenRefreshResult:
            return {"token_data": {"access_token": f"new_token_{call_count}"}, "config_updates": None}

        auth = CustomAuth(header_callback=header_callback, refresh_func=refresh_func, can_refresh_func=lambda: True)

        # Measure header preparation time
        start_time = time.time()
        headers = auth.prepare_request_headers()
        header_time = time.time() - start_time

        # Should be very fast
        assert header_time < 0.01
        assert headers["Authorization"] == "Bearer token_1"

        # Measure refresh time
        start_time = time.time()
        result = auth.refresh()
        refresh_time = time.time() - start_time

        # Should be fast
        assert refresh_time < 0.01
        assert result is not None
        token_data = result.get("token_data")
        assert token_data is not None
        assert token_data.get("access_token") == "new_token_1"

    def test_multiple_refresh_operations(self) -> None:
        """Test performance of multiple refresh operations."""

        # Create a test subclass with fast refresh
        class TestBearerAuth(BearerAuth):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                self.refresh_count = 0

            def refresh(self) -> api_types.TokenRefreshResult:
                self.refresh_count += 1
                self.access_token = f"token_{self.refresh_count}"
                return {"token_data": {"access_token": self.access_token}, "config_updates": None}

        auth = TestBearerAuth(access_token="initial_token", http_request_callable=Mock())

        # Measure time for multiple refreshes
        start_time = time.time()
        for _ in range(10):
            auth.refresh()
        total_time = time.time() - start_time

        # Should complete all refreshes quickly
        assert total_time < 0.1
        assert auth.refresh_count == 10
        assert auth.access_token == "token_10"

    def test_callback_invocation_performance(self) -> None:
        """Test performance of callback invocation."""

        # Create a test subclass with fast refresh
        class TestBearerAuth(BearerAuth):
            def refresh(self) -> api_types.TokenRefreshResult:
                self.access_token = "refreshed_token"
                return {"token_data": {"access_token": "refreshed_token"}, "config_updates": None}

        auth = TestBearerAuth(access_token="initial_token", http_request_callable=Mock())

        callback = auth.get_refresh_callback()
        assert callback is not None

        # Measure callback invocation time
        start_time = time.time()
        callback()
        callback_time = time.time() - start_time

        # Should be very fast
        assert callback_time < 0.01
        assert auth.access_token == "refreshed_token"
