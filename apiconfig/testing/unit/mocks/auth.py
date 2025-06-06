# -*- coding: utf-8 -*-
"""Mock implementations of authentication strategies for testing."""

import random
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

from apiconfig.auth.base import AuthStrategy
from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.exceptions.auth import TokenRefreshError
from apiconfig.types import AuthRefreshCallback, TokenRefreshResult


class MockAuthStrategy(AuthStrategy):
    """
    Base mock implementation for AuthStrategy for testing purposes.

    Handles common mocking logic like overriding headers/params and raising exceptions.
    Specific mock strategies should inherit from this class.
    """

    override_headers: Dict[str, str]
    override_params: Dict[str, Any]
    raise_exception: Optional[Exception]

    def __init__(
        self,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the MockAuthStrategy.

        Args
        ----
        override_headers
            Optional dictionary of headers to add/override in the result.
        override_params
            Optional dictionary of parameters to add/override in the result.
        raise_exception
            Optional exception instance to raise when prepare_request is called.
        """
        self.override_headers = override_headers if override_headers is not None else {}
        self.override_params = override_params if override_params is not None else {}
        self.raise_exception = raise_exception

    def prepare_request(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Prepare request headers and parameters, applying mock configurations.

        If `raise_exception` was provided during initialization, it will be raised.
        Otherwise, it merges the input headers/params with the `override_headers`
        and `override_params` provided during initialization.

        Args
        ----
        headers
            Existing request headers.
        params
            Existing request parameters.

        Returns
        -------
        Tuple[Dict[str, str], Dict[str, Any]]
            A tuple containing the prepared headers and parameters dictionaries.

        Raises
        ------
        Exception
            The exception provided via `raise_exception` during init.
        """
        if self.raise_exception:
            raise self.raise_exception

        final_headers = headers.copy() if headers else {}
        final_headers.update(self.override_headers)

        final_params = params.copy() if params else {}
        final_params.update(self.override_params)

        return final_headers, final_params

    def prepare_request_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Provide a dummy implementation required by AuthStrategy ABC."""
        current_headers = headers if headers is not None else {}
        return current_headers

    def prepare_request_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Provide a dummy implementation required by AuthStrategy ABC."""
        current_params = params if params is not None else {}
        return current_params


class MockBasicAuth(MockAuthStrategy, BasicAuth):
    """Mock implementation of BasicAuth."""

    def __init__(
        self,
        username: str = "testuser",
        password: str = "testpass",
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the MockBasicAuth strategy.

        Args
        ----
        username
            The mock username (passed to real BasicAuth init).
        password
            The mock password (passed to real BasicAuth init).
        override_headers
            Optional dictionary of headers to add/override in the result.
        override_params
            Optional dictionary of parameters to add/override in the result.
        raise_exception
            Optional exception instance to raise when prepare_request is called.
        """
        BasicAuth.__init__(self, username, password)
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy


class MockBearerAuth(MockAuthStrategy, BearerAuth):
    """Mock implementation of BearerAuth."""

    def __init__(
        self,
        token: str = "testtoken",
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the MockBearerAuth strategy.

        Args
        ----
        token
            The mock bearer token (passed to real BearerAuth init).
        override_headers
            Optional dictionary of headers to add/override in the result.
        override_params
            Optional dictionary of parameters to add/override in the result.
        raise_exception
            Optional exception instance to raise when prepare_request is called.
        """
        BearerAuth.__init__(self, token)
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy


class MockApiKeyAuth(MockAuthStrategy, ApiKeyAuth):
    """Mock implementation of ApiKeyAuth."""

    def __init__(
        self,
        api_key: str = "testapikey",
        header_name: str = "X-API-Key",
        param_name: Optional[str] = None,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the MockApiKeyAuth strategy.

        Args
        ----
        api_key
            The mock API key (passed to real ApiKeyAuth init).
        header_name
            The header name (passed to real ApiKeyAuth init).
        param_name
            The query parameter name (passed to real ApiKeyAuth init).
        override_headers
            Optional dictionary of headers to add/override in the result.
        override_params
            Optional dictionary of parameters to add/override in the result.
        raise_exception
            Optional exception instance to raise when prepare_request is called.
        """
        ApiKeyAuth.__init__(self, api_key, header_name, param_name)
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy


class MockRefreshableAuthStrategy(MockAuthStrategy):
    """Mock auth strategy with refresh capabilities for testing."""

    def __init__(
        self,
        initial_token: str = "mock_token",
        refresh_token: str = "mock_refresh",
        can_refresh: bool = True,
        refresh_success: bool = True,
        refresh_delay: float = 0.0,
        max_refresh_attempts: int = 3,
        **kwargs: Any,
    ) -> None:
        """Initialize the MockRefreshableAuthStrategy.

        Parameters
        ----------
        initial_token : str, optional
            The initial access token, by default "mock_token".
        refresh_token : str, optional
            The refresh token, by default "mock_refresh".
        can_refresh : bool, optional
            Whether refresh is supported, by default True.
        refresh_success : bool, optional
            Whether refresh operations should succeed, by default True.
        refresh_delay : float, optional
            Delay in seconds for refresh operations, by default 0.0.
        max_refresh_attempts : int, optional
            Maximum number of refresh attempts allowed, by default 3.
        **kwargs
            Additional arguments passed to MockAuthStrategy.
        """
        super().__init__(**kwargs)
        self.initial_token = initial_token
        self.current_token = initial_token
        self.refresh_token = refresh_token
        self._can_refresh = can_refresh
        self._refresh_success = refresh_success
        self._refresh_delay = refresh_delay
        self._max_refresh_attempts = max_refresh_attempts
        self._refresh_attempts = 0
        self._is_expired = False
        self._expiry_time: Optional[float] = None

    def can_refresh(self) -> bool:
        """Check if this auth strategy supports refresh and is configured to do so.

        Returns
        -------
        bool
            True if refresh is supported and possible, False otherwise.
        """
        return self._can_refresh and self._refresh_attempts < self._max_refresh_attempts

    def is_expired(self) -> bool:
        """Check if current credentials are known to be expired.

        Returns
        -------
        bool
            True if credentials are known to be expired, False otherwise.
        """
        # Check timestamp-based expiry first
        if self._expiry_time is not None and time.time() >= self._expiry_time:
            return True
        return self._is_expired

    def set_expired(self, expired: bool = True) -> None:
        """Set token expiration state for testing.

        Parameters
        ----------
        expired : bool, optional
            Whether the token should be marked as expired, by default True.
        """
        self._is_expired = expired

    def refresh(self) -> Optional[TokenRefreshResult]:
        """Mock refresh implementation with configurable behavior.

        Returns
        -------
        Optional[TokenRefreshResult]
            A structure containing token data and optional config updates,
            or None if refresh fails.

        Raises
        ------
        TokenRefreshError
            If refresh fails due to configuration or attempt limits.
        """
        if self._refresh_delay > 0:
            time.sleep(self._refresh_delay)

        # Check if refresh is available before incrementing attempts
        if not self.can_refresh():
            raise TokenRefreshError("Mock refresh not available")

        self._refresh_attempts += 1

        if not self._refresh_success:
            raise TokenRefreshError("Mock refresh failure")

        # Generate new token
        new_token = f"{self.initial_token}_refreshed_{self._refresh_attempts}"
        self.current_token = new_token
        self._is_expired = False

        return {
            "token_data": {"access_token": new_token, "refresh_token": f"{self.refresh_token}_new", "expires_in": 3600, "token_type": "Bearer"},
            "config_updates": None,
        }

    def get_refresh_callback(self) -> Optional[AuthRefreshCallback]:
        """Return a mock refresh callback that uses this strategy's refresh method.

        Returns
        -------
        Optional[AuthRefreshCallback]
            A callable that performs refresh when called, or None if refresh
            is not supported.
        """
        if not self.can_refresh():
            return None

        def _mock_callback() -> None:
            """Wrap refresh operation for callback usage."""
            refreshed_token_result = self.refresh()
            if refreshed_token_result is None:
                raise TokenRefreshError("Mock callback: Refresh method returned None unexpectedly.")

        return _mock_callback

    def apply_auth(self, headers: Dict[str, str]) -> None:
        """Apply authentication to headers (base implementation).

        Parameters
        ----------
        headers : Dict[str, str]
            The headers dictionary to modify.
        """
        # Base implementation - subclasses should override
        headers["Authorization"] = f"Mock {self.current_token}"


class MockBearerAuthWithRefresh(MockRefreshableAuthStrategy):
    """Mock Bearer auth with refresh capabilities."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the MockBearerAuthWithRefresh strategy.

        Parameters
        ----------
        **kwargs
            Arguments passed to MockRefreshableAuthStrategy.
        """
        super().__init__(**kwargs)

    def apply_auth(self, headers: Dict[str, str]) -> None:
        """Apply Bearer authentication to headers.

        Parameters
        ----------
        headers : Dict[str, str]
            The headers dictionary to modify.
        """
        headers["Authorization"] = f"Bearer {self.current_token}"


class MockApiKeyAuthWithRefresh(MockRefreshableAuthStrategy):
    """Mock API Key auth with refresh capabilities."""

    def __init__(self, header_name: str = "X-API-Key", **kwargs: Any) -> None:
        """Initialize the MockApiKeyAuthWithRefresh strategy.

        Parameters
        ----------
        header_name : str, optional
            The header name for the API key, by default "X-API-Key".
        **kwargs
            Arguments passed to MockRefreshableAuthStrategy.
        """
        super().__init__(**kwargs)
        self.header_name = header_name

    def apply_auth(self, headers: Dict[str, str]) -> None:
        """Apply API Key authentication to headers.

        Parameters
        ----------
        headers : Dict[str, str]
            The headers dictionary to modify.
        """
        headers[self.header_name] = self.current_token


class MockCustomAuthWithRefresh(MockRefreshableAuthStrategy):
    """Mock Custom auth with configurable refresh behavior."""

    def __init__(self, auth_header_format: str = "Custom {token}", **kwargs: Any) -> None:
        """Initialize the MockCustomAuthWithRefresh strategy.

        Parameters
        ----------
        auth_header_format : str, optional
            Format string for the authorization header, by default "Custom {token}".
        **kwargs
            Arguments passed to MockRefreshableAuthStrategy.
        """
        super().__init__(**kwargs)
        self.auth_header_format = auth_header_format

    def apply_auth(self, headers: Dict[str, str]) -> None:
        """Apply Custom authentication to headers.

        Parameters
        ----------
        headers : Dict[str, str]
            The headers dictionary to modify.
        """
        headers["Authorization"] = self.auth_header_format.format(token=self.current_token)


class MockAuthErrorInjector:
    """Utility for injecting errors into mock auth strategies."""

    @staticmethod
    def create_failing_refresh_strategy(failure_type: str = "network", failure_after_attempts: int = 1, **kwargs: Any) -> MockBearerAuthWithRefresh:
        """Create a mock strategy that fails refresh after specified attempts.

        Parameters
        ----------
        failure_type : str, optional
            Type of failure ("network", "auth", "timeout"), by default "network".
        failure_after_attempts : int, optional
            Number of successful attempts before failure, by default 1.
        **kwargs
            Additional arguments for mock strategy.

        Returns
        -------
        MockBearerAuthWithRefresh
            A mock strategy configured to fail after the specified attempts.
        """
        strategy = MockBearerAuthWithRefresh(**kwargs)
        original_refresh = strategy.refresh

        def failing_refresh() -> Optional[TokenRefreshResult]:
            if strategy._refresh_attempts >= failure_after_attempts:
                if failure_type == "network":
                    raise ConnectionError("Mock network failure")
                elif failure_type == "auth":
                    raise TokenRefreshError("Mock authentication failure")
                elif failure_type == "timeout":
                    raise TimeoutError("Mock timeout failure")
                else:
                    raise Exception(f"Mock {failure_type} failure")
            return original_refresh()

        strategy.refresh = failing_refresh  # type: ignore[method-assign]
        return strategy

    @staticmethod
    def create_intermittent_failure_strategy(failure_probability: float = 0.3, **kwargs: Any) -> MockBearerAuthWithRefresh:
        """Create a strategy with intermittent refresh failures.

        Parameters
        ----------
        failure_probability : float, optional
            Probability of failure (0.0 to 1.0), by default 0.3.
        **kwargs
            Additional arguments for mock strategy.

        Returns
        -------
        MockBearerAuthWithRefresh
            A mock strategy configured with intermittent failures.
        """
        strategy = MockBearerAuthWithRefresh(**kwargs)
        original_refresh = strategy.refresh

        def intermittent_refresh() -> Optional[TokenRefreshResult]:
            if random.random() < failure_probability:
                raise TokenRefreshError("Mock intermittent failure")
            return original_refresh()

        strategy.refresh = intermittent_refresh  # type: ignore[method-assign]
        return strategy


class AuthTestScenarioBuilder:
    """Builder for creating complex auth test scenarios."""

    @staticmethod
    def create_token_expiry_scenario(initial_token: str = "initial_token", expires_after_seconds: float = 1.0) -> MockBearerAuthWithRefresh:
        """Create a scenario where token expires after specified time.

        Parameters
        ----------
        initial_token : str, optional
            The initial token value, by default "initial_token".
        expires_after_seconds : float, optional
            Time in seconds after which token expires, by default 1.0.

        Returns
        -------
        MockBearerAuthWithRefresh
            A mock strategy configured to expire after the specified time.
        """
        strategy = MockBearerAuthWithRefresh(initial_token=initial_token)

        # Set expiry time based on current time + expiry duration
        # This avoids race conditions with background threads
        strategy._expiry_time = time.time() + expires_after_seconds
        return strategy

    @staticmethod
    def create_concurrent_refresh_scenario(num_concurrent_refreshes: int = 5) -> MockBearerAuthWithRefresh:
        """Create a scenario for testing concurrent refresh operations.

        Parameters
        ----------
        num_concurrent_refreshes : int, optional
            Number of concurrent refreshes to support, by default 5.

        Returns
        -------
        MockBearerAuthWithRefresh
            A mock strategy configured for concurrent refresh testing.
        """
        strategy = MockBearerAuthWithRefresh(max_refresh_attempts=num_concurrent_refreshes + 5)

        # Add thread safety tracking
        strategy._refresh_lock = threading.Lock()  # type: ignore[attr-defined]
        strategy._concurrent_refreshes = 0  # type: ignore[attr-defined]
        strategy._max_concurrent_refreshes = 0  # type: ignore[attr-defined]

        original_refresh = strategy.refresh

        def thread_safe_refresh() -> Optional[TokenRefreshResult]:
            with strategy._refresh_lock:  # type: ignore[attr-defined]
                strategy._concurrent_refreshes += 1  # type: ignore[attr-defined]
                strategy._max_concurrent_refreshes = max(  # type: ignore[attr-defined]
                    strategy._max_concurrent_refreshes,  # type: ignore[attr-defined]
                    strategy._concurrent_refreshes,  # type: ignore[attr-defined]
                )

            try:
                result = original_refresh()
                return result
            finally:
                with strategy._refresh_lock:  # type: ignore[attr-defined]
                    strategy._concurrent_refreshes -= 1  # type: ignore[attr-defined]

        strategy.refresh = thread_safe_refresh  # type: ignore[method-assign]
        return strategy

    @staticmethod
    def create_crudclient_integration_scenario() -> MockRefreshableAuthStrategy:
        """Create a scenario that mimics crudclient integration patterns.

        Returns
        -------
        MockRefreshableAuthStrategy
            A mock strategy configured for crudclient integration testing.
        """
        strategy = MockRefreshableAuthStrategy()

        # Track callback usage
        strategy._callback_calls = 0  # type: ignore[attr-defined]
        strategy._callback_errors = []  # type: ignore[attr-defined]

        original_get_refresh_callback = strategy.get_refresh_callback

        def tracked_get_refresh_callback() -> Optional[AuthRefreshCallback]:
            callback = original_get_refresh_callback()
            if callback is None:
                return None

            def tracked_callback() -> None:
                strategy._callback_calls += 1  # type: ignore[attr-defined]
                try:
                    return callback()
                except Exception as e:
                    strategy._callback_errors.append(e)  # type: ignore[attr-defined]
                    raise

            return tracked_callback

        strategy.get_refresh_callback = tracked_get_refresh_callback  # type: ignore[method-assign]
        return strategy


class MockHttpRequestCallable:
    """Mock HTTP request callable for testing auth refresh."""

    def __init__(self, responses: Optional[Dict[str, Any]] = None, delay: float = 0.0, failure_rate: float = 0.0) -> None:
        """Initialize the MockHttpRequestCallable.

        Parameters
        ----------
        responses : Optional[Dict[str, Any]], optional
            Predefined responses keyed by "method:url", by default None.
        delay : float, optional
            Delay in seconds for each request, by default 0.0.
        failure_rate : float, optional
            Probability of request failure (0.0 to 1.0), by default 0.0.
        """
        self.responses = responses or {}
        self.delay = delay
        self.failure_rate = failure_rate
        self.call_count = 0
        self.call_history: List[Dict[str, Any]] = []

    def __call__(self, method: str, url: str, **kwargs: Any) -> Any:
        """Mock HTTP request implementation.

        Parameters
        ----------
        method : str
            HTTP method (GET, POST, etc.).
        url : str
            Request URL.
        **kwargs
            Additional request parameters.

        Returns
        -------
        Any
            Mock response object.

        Raises
        ------
        ConnectionError
            If failure rate triggers a mock failure.
        """
        self.call_count += 1
        self.call_history.append({"method": method, "url": url, "kwargs": kwargs})

        if self.delay > 0:
            time.sleep(self.delay)

        if random.random() < self.failure_rate:
            raise ConnectionError("Mock HTTP failure")

        # Return configured response or default
        response_key = f"{method}:{url}"
        if response_key in self.responses:
            response_data = self.responses[response_key]
        else:
            response_data = {
                "access_token": f"mock_token_{self.call_count}",
                "refresh_token": f"mock_refresh_{self.call_count}",
                "expires_in": 3600,
                "token_type": "Bearer",
            }

        # Create mock response object
        class MockResponse:
            def __init__(self, data: Dict[str, Any]) -> None:
                self.data = data
                self.status_code = 200
                self.headers = {"Content-Type": "application/json"}

            def json(self) -> Dict[str, Any]:
                return self.data

        return MockResponse(response_data)


class MockCustomAuth(MockAuthStrategy, CustomAuth):
    """Mock implementation of CustomAuth."""

    def __init__(
        self,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the MockCustomAuth strategy.

        Args
        ----
        override_headers
            Optional dictionary of headers to add/override in the result.
        override_params
            Optional dictionary of parameters to add/override in the result.
        raise_exception
            Optional exception instance to raise when prepare_request is called.
        """
        MockAuthStrategy.__init__(
            self,
            override_headers=override_headers,
            override_params=override_params,
            raise_exception=raise_exception,
        )

    # prepare_request is inherited from MockAuthStrategy
