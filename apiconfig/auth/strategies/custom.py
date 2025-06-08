"""Custom authentication strategy using user-provided callbacks."""

from typing import Callable, Dict, Mapping, Optional

from apiconfig.auth.base import AuthStrategy
from apiconfig.exceptions.auth import AuthStrategyError
from apiconfig.types import HttpRequestCallable, QueryParamType, TokenRefreshResult


class CustomAuth(AuthStrategy):
    """
    Custom authentication strategy with optional refresh capabilities.

    This strategy allows for completely custom authentication logic while
    still supporting the refresh interface for integration with retry mechanisms.

    Examples
    --------
    Basic custom auth without refresh:

    >>> def my_header_callback():
    ...     return {"X-Custom-Auth": "my-secret-token"}
    >>> auth = CustomAuth(header_callback=my_header_callback)

    Custom auth with refresh capabilities:

    >>> current_token = {"value": "initial-token"}
    >>> def my_header_callback():
    ...     return {"Authorization": f"Bearer {current_token['value']}"}
    >>> def my_refresh():
    ...     new_token = fetch_new_token()
    ...     current_token['value'] = new_token
    ...     return {"token_data": {"access_token": new_token}}
    >>> auth = CustomAuth(
    ...     header_callback=my_header_callback,
    ...     refresh_func=my_refresh,
    ...     can_refresh_func=lambda: True
    ... )

    Using factory methods:

    >>> auth = CustomAuth.create_api_key_custom(
    ...     api_key="my-key",
    ...     header_name="X-API-Key"
    ... )
    """

    def __init__(
        self,
        header_callback: Optional[Callable[..., Mapping[str, str]]] = None,
        param_callback: Optional[Callable[..., Mapping[str, str]]] = None,
        refresh_func: Optional[Callable[[], Optional[TokenRefreshResult]]] = None,
        can_refresh_func: Optional[Callable[[], bool]] = None,
        is_expired_func: Optional[Callable[[], bool]] = None,
        http_request_callable: Optional[HttpRequestCallable] = None,
    ) -> None:
        """
        Initialize custom authentication with optional refresh capabilities.

        Parameters
        ----------
        header_callback : Optional[Callable[..., Mapping[str, str]]]
            Function to generate authentication headers. The callback must
            return a mapping of strings.
        param_callback : Optional[Callable[..., Mapping[str, str]]]
            Function to generate authentication parameters. The callback must
            return a mapping of strings.
        refresh_func : Optional[Callable[[], Optional[TokenRefreshResult]]]
            Optional function to perform refresh operations.
        can_refresh_func : Optional[Callable[[], bool]]
            Optional function to check if refresh is possible.
        is_expired_func : Optional[Callable[[], bool]]
            Optional function to check if credentials are expired.
        http_request_callable : Optional[HttpRequestCallable]
            Optional HTTP callable for refresh operations.

        Raises
        ------
        AuthStrategyError
            If neither header_callback nor param_callback is provided.
        """
        super().__init__(http_request_callable)

        # Validate that at least one callback is provided (existing validation)
        if header_callback is None and param_callback is None:
            raise AuthStrategyError("At least one callback (header or param) must be provided for CustomAuth.")

        self._header_callback = header_callback
        self._param_callback = param_callback
        self.refresh_func = refresh_func
        self.can_refresh_func = can_refresh_func
        self.is_expired_func = is_expired_func

    def can_refresh(self) -> bool:
        """
        Check if this custom auth strategy can perform refresh operations.

        Returns
        -------
        bool
            True if refresh function is provided and indicates refresh is possible.
        """
        if self.can_refresh_func is not None:
            return self.can_refresh_func()
        return self.refresh_func is not None

    def is_expired(self) -> bool:
        """
        Check if current credentials are expired.

        Returns
        -------
        bool
            True if expired function indicates expiration, False otherwise.
        """
        if self.is_expired_func is not None:
            return self.is_expired_func()
        return False  # Default to not expired if no function provided

    def refresh(self) -> Optional[TokenRefreshResult]:
        """
        Refresh authentication credentials using the provided refresh function.

        Returns
        -------
        Optional[TokenRefreshResult]
            Result from refresh function or None.

        Raises
        ------
        AuthStrategyError
            If no refresh function is configured or if refresh fails.
        """
        if self.refresh_func is None:
            raise AuthStrategyError("Custom auth strategy has no refresh function configured")

        try:
            return self.refresh_func()
        except Exception as e:
            raise AuthStrategyError(f"Custom auth refresh failed: {str(e)}") from e

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Generate request headers using the header_callback, if provided.

        Enhanced to work with refresh scenarios.

        Returns
        -------
        Dict[str, str]
            A dictionary of headers generated from the callback. The callback
            must return a mapping of strings.

        Raises
        ------
        AuthStrategyError
            If the header_callback fails or returns invalid data.
        """
        if self._header_callback:
            try:
                result = self._header_callback()
                return dict(result)
            except Exception as e:
                raise AuthStrategyError(f"CustomAuth header callback failed: {e}") from e
        return {}

    def prepare_request(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> tuple[Dict[str, str], Dict[str, str]]:
        """
        Prepare authentication headers and parameters for an HTTP request.

        Parameters
        ----------
        headers : Optional[Dict[str, str]]
            Optional initial headers dictionary to update.
        params : Optional[Dict[str, str]]
            Optional initial parameters dictionary to update.

        Returns
        -------
        tuple[Dict[str, str], Dict[str, str]]
            A tuple of (headers, params) dictionaries with authentication data.
        """
        # Initialize headers and params if not provided
        headers = headers.copy() if headers else {}
        params = params.copy() if params else {}

        # Update with authentication headers and params
        headers.update(self.prepare_request_headers())
        auth_params = self.prepare_request_params()
        if auth_params:
            # Convert QueryParamType to Dict[str, str] for compatibility
            for key, value in auth_params.items():
                if value is not None:
                    params[key] = str(value)

        return headers, params

    def prepare_request_params(self) -> Optional[QueryParamType]:
        """
        Generate request parameters using the param_callback, if provided.

        Enhanced to work with refresh scenarios.

        Returns
        -------
        Optional[QueryParamType]
            A dictionary of parameters generated from the callback. The callback
            must return a mapping of strings.

        Raises
        ------
        AuthStrategyError
            If the param_callback fails or returns invalid data.
        """
        if self._param_callback:
            try:
                result = self._param_callback()
                return dict(result)
            except Exception as e:
                raise AuthStrategyError(f"CustomAuth parameter callback failed: {e}") from e
        return {}

    @classmethod
    def create_api_key_custom(
        cls,
        api_key: str,
        header_name: str = "X-API-Key",
        http_request_callable: Optional[HttpRequestCallable] = None,
    ) -> "CustomAuth":
        """
        Create a custom auth strategy for simple API key authentication.

        Parameters
        ----------
        api_key : str
            The API key value.
        header_name : str, optional
            Header name for the API key (default: "X-API-Key").
        http_request_callable : Optional[HttpRequestCallable], optional
            Optional HTTP callable for operations.

        Returns
        -------
        CustomAuth
            Configured custom auth strategy.
        """

        def header_callback() -> Dict[str, str]:
            return {header_name: api_key}

        return cls(header_callback=header_callback, http_request_callable=http_request_callable)

    @classmethod
    def create_session_token_custom(
        cls,
        session_token: str,
        session_refresh_func: Callable[[], str],
        header_name: str = "Authorization",
        token_prefix: str = "Session",
        http_request_callable: Optional[HttpRequestCallable] = None,
    ) -> "CustomAuth":
        """
        Create a custom auth strategy for session token authentication with refresh.

        Parameters
        ----------
        session_token : str
            Initial session token.
        session_refresh_func : Callable[[], str]
            Function to refresh the session token.
        header_name : str, optional
            Header name for the token (default: "Authorization").
        token_prefix : str, optional
            Prefix for the token value (default: "Session").
        http_request_callable : Optional[HttpRequestCallable], optional
            Optional HTTP callable for refresh operations.

        Returns
        -------
        CustomAuth
            Configured custom auth strategy.
        """
        current_token = {"token": session_token}

        def header_callback() -> Dict[str, str]:
            return {header_name: f"{token_prefix} {current_token['token']}"}

        def refresh_func() -> Optional[TokenRefreshResult]:
            new_token = session_refresh_func()
            current_token["token"] = new_token

            return {"token_data": {"access_token": new_token, "token_type": "session"}, "config_updates": None}

        return cls(
            header_callback=header_callback, refresh_func=refresh_func, can_refresh_func=lambda: True, http_request_callable=http_request_callable
        )
