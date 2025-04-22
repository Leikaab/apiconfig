# -*- coding: utf-8 -*-
"""Mock implementations of authentication strategies for testing."""

from typing import Any, Dict, Optional, Tuple

from apiconfig.auth.base import AuthStrategy
from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth


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
