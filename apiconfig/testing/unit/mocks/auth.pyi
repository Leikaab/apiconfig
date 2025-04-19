# Stub file for apiconfig/testing/unit/mocks/auth.py
# Contains docstrings and public type hints

from typing import Any, Dict, Optional, Tuple

from apiconfig.auth.base import AuthStrategy
from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.exceptions.auth import AuthenticationError


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
        """
        Initialize the MockAuthStrategy.

        Args:
            override_headers: Optional dictionary of headers to add/override in the result.
            override_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """
        Prepare request headers and parameters, applying mock configurations.

        If `raise_exception` was provided during initialization, it will be raised.
        Otherwise, it merges the input headers/params with the `override_headers`
        and `override_params` provided during initialization.

        Args:
            headers: Existing request headers.
            params: Existing request parameters.

        Returns:
            A tuple containing the prepared headers and parameters dictionaries.

        Raises:
            Exception: The exception provided via `raise_exception` during init.
        """
        ...

    # Add signatures for dummy implementations required by AuthStrategy ABC
    def prepare_request_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Dummy implementation required by AuthStrategy ABC."""
        ...

    def prepare_request_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dummy implementation required by AuthStrategy ABC."""
        ...


class MockBasicAuth(MockAuthStrategy, BasicAuth):
    """
    Mock implementation of BasicAuth inheriting mock behavior from MockAuthStrategy.
    """
    # Attributes like override_headers are inherited from MockAuthStrategy

    def __init__(
        self,
        username: str = "testuser",
        password: str = "testpass",
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockBasicAuth strategy.

        Args:
            username: The mock username (passed to real BasicAuth init).
            password: The mock password (passed to real BasicAuth init).
            override_headers: Optional dictionary of headers to add/override in the result.
            override_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    # prepare_request is inherited from MockAuthStrategy
    # Docstring for prepare_request is also inherited implicitly,
    # but could be overridden if specific mock behavior needed description.


class MockBearerAuth(MockAuthStrategy, BearerAuth):
    """
    Mock implementation of BearerAuth inheriting mock behavior from MockAuthStrategy.
    """
    # Attributes inherited from MockAuthStrategy

    def __init__(
        self,
        token: str = "testtoken",
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockBearerAuth strategy.

        Args:
            token: The mock bearer token (passed to real BearerAuth init).
            override_headers: Optional dictionary of headers to add/override in the result.
            override_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    # prepare_request is inherited from MockAuthStrategy


class MockApiKeyAuth(MockAuthStrategy, ApiKeyAuth):
    """
    Mock implementation of ApiKeyAuth inheriting mock behavior from MockAuthStrategy.
    """
    # Attributes inherited from MockAuthStrategy

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
        """
        Initialize the MockApiKeyAuth strategy.

        Args:
            api_key: The mock API key (passed to real ApiKeyAuth init).
            header_name: The header name (passed to real ApiKeyAuth init).
            param_name: The query parameter name (passed to real ApiKeyAuth init).
            override_headers: Optional dictionary of headers to add/override in the result.
            override_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    # prepare_request is inherited from MockAuthStrategy


class MockCustomAuth(MockAuthStrategy, CustomAuth):
    """
    Mock implementation of CustomAuth inheriting mock behavior from MockAuthStrategy.
    """
    # Attributes inherited from MockAuthStrategy

    def __init__(
        self,
        *,
        override_headers: Optional[Dict[str, str]] = None,
        override_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockCustomAuth strategy.

        Args:
            override_headers: Optional dictionary of headers to add/override in the result.
            override_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    # prepare_request is inherited from MockAuthStrategy
