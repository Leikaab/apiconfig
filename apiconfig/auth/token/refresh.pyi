from typing import Any, Dict, Optional, Tuple

from ...config.base import ClientConfig
from ...exceptions.auth import (
    TokenRefreshError,
    TokenRefreshJsonError,
    TokenRefreshNetworkError,
    TokenRefreshTimeoutError,
)


def _extract_json_from_response(response: Any) -> Dict[str, Any]: ...


def _check_http_status(response: Any) -> None: ...


def _handle_exception(e: Exception) -> None: ...


def _make_token_refresh_request(
    token_url: str,
    payload: Dict[str, Any],
    auth: Optional[Any] = ...,
    timeout: float = ...,
    http_client: Optional[Any] = ...,
) -> Dict[str, Any]: ...


def _get_effective_settings(
    timeout: Optional[float],
    max_retries: Optional[int],
    client_config: Optional[ClientConfig],
) -> Tuple[float, int]: ...


def _prepare_auth_and_payload(
    client_id: Optional[str],
    client_secret: Optional[str],
    refresh_token: str,
    extra_params: Optional[Dict[str, Any]],
    http_client: Optional[Any],
) -> Tuple[Optional[Any], Dict[str, Any]]: ...


def _execute_with_retry(
    token_url: str,
    payload: Dict[str, Any],
    auth: Optional[Any],
    timeout: float,
    max_retries: int,
    http_client: Optional[Any],
) -> Dict[str, Any]: ...


def refresh_oauth2_token(
    refresh_token: str,
    token_url: str,
    client_id: Optional[str] = ...,
    client_secret: Optional[str] = ...,
    extra_params: Optional[Dict[str, Any]] = ...,
    timeout: Optional[float] = ...,
    max_retries: Optional[int] = ...,
    client_config: Optional[ClientConfig] = ...,
    http_client: Optional[Any] = ...,
) -> Dict[str, Any]:
    """
    Refreshes an OAuth2 token using a refresh token.

    This function implements the standard OAuth2 refresh token grant type flow.
    It constructs the necessary payload and makes an HTTP POST request to the
    token endpoint with timeout and retry capabilities.

    Args:
        refresh_token: The refresh token obtained during the initial authorization.
        token_url: The URL of the authorization server's token endpoint.
        client_id: The client identifier issued to the client during registration.
            Optional, depending on the provider's requirements.
        client_secret: The client secret. Optional and should be used carefully,
            typically only for confidential clients.
        extra_params: Additional parameters to include in the request body,
            as required by the specific authorization server.
        timeout: Request timeout in seconds. If not provided, uses the value from
            client_config or the default (10.0).
        max_retries: Maximum number of retry attempts for transient errors.
            If not provided, uses the value from client_config or the default (3).
        client_config: Optional ClientConfig instance to use for timeout and retry settings.
        http_client: An HTTP client instance to use for making the request.
            This is required as apiconfig does not include HTTP client dependencies.

    Returns:
        A dictionary containing the new token information (e.g., access_token,
        expires_in, potentially a new refresh_token).

    Raises:
        TokenRefreshError: If the token refresh fails (e.g., invalid refresh token,
            server error, invalid response).
        TokenRefreshJsonError: If the response cannot be parsed as JSON.
        TokenRefreshTimeoutError: If the request times out.
        TokenRefreshNetworkError: If there's a network-related error.
    """
    ...
