"""Test refresh interface consistency across auth strategies."""

from unittest.mock import Mock as MockClass

import apiconfig.types as api_types
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth


class TestAuthRefreshInterface:
    """Test refresh interface consistency across auth strategies."""

    def test_refresh_interface_consistency(self) -> None:
        """Test that all refreshable strategies implement consistent interface."""
        # Mock HTTP callable
        mock_http = MockClass()
        mock_http.return_value = MockClass(json=lambda: {"access_token": "new_token", "refresh_token": "new_refresh", "expires_in": 3600})

        # Create a test subclass of BearerAuth that implements refresh
        class TestBearerAuth(BearerAuth):
            def refresh(self) -> api_types.TokenRefreshResult:
                return {"token_data": {"access_token": "new_token"}, "config_updates": None}

        strategies = [
            TestBearerAuth(access_token="old_token", http_request_callable=mock_http),
            CustomAuth(
                header_callback=lambda: {"Authorization": "Bearer token"},
                refresh_func=lambda: {"token_data": {"access_token": "new_token"}, "config_updates": None},
                can_refresh_func=lambda: True,
                http_request_callable=mock_http,
            ),
        ]

        for strategy in strategies:
            # Test interface methods exist
            assert hasattr(strategy, "can_refresh")
            assert hasattr(strategy, "refresh")
            assert hasattr(strategy, "is_expired")
            assert hasattr(strategy, "get_refresh_callback")

            # Test refresh capability
            if strategy.can_refresh():
                callback = strategy.get_refresh_callback()
                assert callback is not None
                assert callable(callback)

                # Test refresh returns proper structure
                result = strategy.refresh()
                assert isinstance(result, dict)
                assert "token_data" in result
                assert "config_updates" in result

    def test_crudclient_callback_compatibility(self) -> None:
        """Test compatibility with crudclient's setup_auth_func pattern."""
        mock_http = MockClass()
        mock_http.return_value = MockClass(json=lambda: {"access_token": "new_token", "expires_in": 3600})

        # Create a test subclass that implements refresh
        class TestBearerAuth(BearerAuth):
            def refresh(self) -> api_types.TokenRefreshResult:
                # old_token = self.access_token  # Unused variable
                self.access_token = "new_token"
                return {"token_data": {"access_token": "new_token"}, "config_updates": None}

        auth = TestBearerAuth(access_token="old_token", http_request_callable=mock_http)

        # Get callback (simulating crudclient usage)
        setup_auth_func = auth.get_refresh_callback()
        assert setup_auth_func is not None

        # Test callback signature matches crudclient expectation
        import inspect

        sig = inspect.signature(setup_auth_func)
        assert len(sig.parameters) == 0  # No parameters
        assert sig.return_annotation in (None, type(None))  # No return value

        # Test callback execution
        old_token = auth.access_token
        setup_auth_func()  # Should refresh without error

        # Verify token was updated
        assert auth.access_token != old_token
