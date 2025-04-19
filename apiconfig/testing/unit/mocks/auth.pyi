# Stub file for apiconfig/testing/unit/mocks/auth.py
# Contains docstrings and public type hints

from typing import Any, Dict, Optional, Tuple, Union

from apiconfig.auth.strategies.api_key import ApiKeyAuth
from apiconfig.auth.strategies.basic import BasicAuth
from apiconfig.auth.strategies.bearer import BearerAuth
from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.exceptions.auth import AuthenticationError


class MockBasicAuth(BasicAuth):
    """
    Mock implementation of BasicAuth for testing purposes.

    Allows configuring specific return values or exceptions to simulate
    different authentication scenarios during unit tests.
    """
    _return_headers: Optional[Dict[str, str]]
    _return_params: Optional[Dict[str, Any]]
    _raise_exception: Optional[Exception]

    def __init__(
        self,
        username: str = "testuser",
        password: str = "testpass",
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockBasicAuth strategy.

        Args:
            username: The mock username.
            password: The mock password.
            return_headers: Optional dictionary of headers to add/override in the result.
            return_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """
        Prepare request headers and parameters, applying mock configurations.

        If `raise_exception` was provided during initialization, it will be raised.
        Otherwise, it returns the standard BasicAuth headers/params, potentially
        updated with `return_headers` and `return_params`.

        Args:
            headers: Existing request headers.
            params: Existing request parameters.

        Returns:
            A tuple containing the prepared headers and parameters dictionaries.

        Raises:
            Exception: The exception provided via `raise_exception` during init.
        """
        ...


class MockBearerAuth(BearerAuth):
    """
    Mock implementation of BearerAuth for testing purposes.

    Allows configuring specific return values or exceptions to simulate
    different authentication scenarios during unit tests.
    """
    _return_headers: Optional[Dict[str, str]]
    _return_params: Optional[Dict[str, Any]]
    _raise_exception: Optional[Exception]

    def __init__(
        self,
        token: str = "testtoken",
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockBearerAuth strategy.

        Args:
            token: The mock bearer token.
            return_headers: Optional dictionary of headers to add/override in the result.
            return_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """
        Prepare request headers and parameters, applying mock configurations.

        If `raise_exception` was provided during initialization, it will be raised.
        Otherwise, it returns the standard BearerAuth headers/params, potentially
        updated with `return_headers` and `return_params`.

        Args:
            headers: Existing request headers.
            params: Existing request parameters.

        Returns:
            A tuple containing the prepared headers and parameters dictionaries.

        Raises:
            Exception: The exception provided via `raise_exception` during init.
        """
        ...


class MockApiKeyAuth(ApiKeyAuth):
    """
    Mock implementation of ApiKeyAuth for testing purposes.

    Allows configuring specific return values or exceptions to simulate
    different authentication scenarios during unit tests.
    """
    _return_headers: Optional[Dict[str, str]]
    _return_params: Optional[Dict[str, Any]]
    _raise_exception: Optional[Exception]

    def __init__(
        self,
        api_key: str = "testapikey",
        header_name: str = "X-API-Key",
        param_name: Optional[str] = None,
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockApiKeyAuth strategy.

        Args:
            api_key: The mock API key.
            header_name: The header name to use for the API key (if not using param_name).
            param_name: The query parameter name to use for the API key (if not using header_name).
            return_headers: Optional dictionary of headers to add/override in the result.
            return_params: Optional dictionary of parameters to add/override in the result.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """
        Prepare request headers and parameters, applying mock configurations.

        If `raise_exception` was provided during initialization, it will be raised.
        Otherwise, it returns the standard ApiKeyAuth headers/params, potentially
        updated with `return_headers` and `return_params`.

        Args:
            headers: Existing request headers.
            params: Existing request parameters.

        Returns:
            A tuple containing the prepared headers and parameters dictionaries.

        Raises:
            Exception: The exception provided via `raise_exception` during init.
        """
        ...


class MockCustomAuth(CustomAuth):
    """
    Mock implementation of CustomAuth for testing purposes.

    Allows configuring specific return values or exceptions to simulate
    different authentication scenarios during unit tests without needing
    a real callback function.
    """
    _return_headers: Dict[str, str]
    _return_params: Dict[str, Any]
    _raise_exception: Optional[Exception]

    def __init__(
        self,
        *,
        return_headers: Optional[Dict[str, str]] = None,
        return_params: Optional[Dict[str, Any]] = None,
        raise_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the MockCustomAuth strategy.

        Args:
            return_headers: Optional dictionary of headers to return. Defaults to empty dict.
            return_params: Optional dictionary of parameters to return. Defaults to empty dict.
            raise_exception: Optional exception instance to raise when prepare_request is called.
        """
        ...

    def prepare_request(
        self, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """
        Prepare request headers and parameters based on mock configurations.

        If `raise_exception` was provided during initialization, it will be raised.
        Otherwise, it returns the headers/params provided during initialization,
        merged with any input headers/params.

        Args:
            headers: Existing request headers.
            params: Existing request parameters.

        Returns:
            A tuple containing the prepared headers and parameters dictionaries.

        Raises:
            Exception: The exception provided via `raise_exception` during init.
        """
        ...
