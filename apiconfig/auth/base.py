# -*- coding: utf-8 -*-
"""Abstract base class for authentication strategies."""

from abc import ABC, abstractmethod
from typing import Dict, Optional

from apiconfig.types import (
    AuthRefreshCallback,
    HttpRequestCallable,
    QueryParamType,
    TokenRefreshResult,
)


class AuthStrategy(ABC):
    """
    Abstract base class for defining authentication strategies.

    This class provides a common interface for different authentication
    methods (e.g., Basic Auth, Bearer Token, API Key). Subclasses must
    implement the abstract methods to provide the specific logic for
    preparing request headers and/or parameters.
    """

    def __init__(self, http_request_callable: Optional[HttpRequestCallable] = None):
        """
        Initialize the AuthStrategy.

        Parameters
        ----------
        http_request_callable : Optional[HttpRequestCallable], optional
            An optional callable that the strategy can use to make HTTP requests
            (e.g., for token refresh). This callable should handle the actual HTTP
            communication. Its signature should be compatible with the needs of
            the refresh mechanism (e.g., taking URL, method, data, headers).
        """
        self._http_request_callable = http_request_callable

    @abstractmethod
    def prepare_request_headers(self) -> Dict[str, str]:
        """Prepare authentication headers for an HTTP request.

        This method should generate the necessary HTTP headers required
        by the specific authentication strategy.

        Raises
        ------
        AuthStrategyError
            If headers cannot be prepared (e.g., missing credentials).

        Returns
        -------
        Dict[str, str]
            A dictionary containing header names and values. An empty
            dictionary should be returned if the strategy does not require headers.
        """
        pass  # pragma: no cover

    def can_refresh(self) -> bool:
        """
        Check if this auth strategy supports refresh and is configured to do so.

        A strategy can refresh if it implements refresh logic AND has been
        provided with necessary components (like an _http_request_callable).

        Returns
        -------
        bool
            True if refresh is supported and possible, False otherwise.
        """
        return False

    def refresh(self) -> Optional[TokenRefreshResult]:
        """
        Refresh authentication credentials.

        This method will typically use the injected _http_request_callable
        to perform the refresh operation (e.g., call a token refresh endpoint).
        It should update the strategy's internal state with the new access token.

        Returns
        -------
        Optional[TokenRefreshResult]
            A structure containing:
            - 'token_data': RefreshedTokenData with the new access token,
              potentially a new refresh token, expiry time, etc.
              The application is responsible for persisting the new refresh
              token (if provided) using a TokenStorage implementation.
            - 'config_updates': Optional dictionary of configuration values
              (e.g., a new API endpoint URL) that were updated during the
              refresh process. The calling client would be responsible for applying these.
            Returns None if refresh is not supported, fails critically, or if
            there's nothing to return.

        Raises
        ------
        NotImplementedError
            If the strategy does not support refresh.
        TokenRefreshError
            If refresh fails due to invalid credentials or network issues.
        AuthStrategyError
            If refresh fails due to strategy-specific issues.
        """
        raise NotImplementedError("This auth strategy does not support refresh")

    def is_expired(self) -> bool:
        """
        Check if current credentials are known to be expired.

        This might involve checking an expiry timestamp if available.

        Returns
        -------
        bool
            True if credentials are known to be expired, False otherwise.
            Returns False by default if expiry cannot be determined.
        """
        return False

    def get_refresh_callback(self) -> Optional[AuthRefreshCallback]:
        """
        Get a callback function suitable for crudclient's setup_auth_func parameter.

        This allows the retry mechanism to trigger this strategy's refresh logic.

        Returns
        -------
        Optional[AuthRefreshCallback]
            A callable that performs refresh when called, or None if refresh
            is not supported.
        """
        if self.can_refresh():

            def refresh_callback() -> None:
                """Wrap refresh operation for callback usage."""
                self.refresh()

            return refresh_callback
        return None

    @abstractmethod
    def prepare_request_params(self) -> Optional[QueryParamType]:
        """Prepare authentication parameters for an HTTP request (e.g., query params).

        This method should generate the necessary request parameters (like
        query parameters) required by the specific authentication strategy.

        Raises
        ------
        AuthStrategyError
            If parameters cannot be prepared (e.g., missing credentials).

        Returns
        -------
        Optional[QueryParamType]
            A dictionary containing parameter names and values, or None if the
            strategy does not require parameters. An empty dictionary may also
            be returned if the strategy does not require parameters.
        """
        pass  # pragma: no cover
