"""
Module for handling OAuth2 token refreshing.

This module provides functionality to refresh OAuth2 access tokens using a refresh token
and handles potential network, timeout, and JSON decoding errors during the process.
It includes retry logic for transient errors.
"""

import json
import logging
import time

# Import httpx only for type annotations, not for actual use
# This allows for proper type checking without runtime dependency
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, cast

if TYPE_CHECKING:
    pass

from ...config.base import ClientConfig
from ...exceptions.auth import (
    TokenRefreshError,
    TokenRefreshJsonError,
    TokenRefreshNetworkError,
    TokenRefreshTimeoutError,
)

# Set up logging
logger = logging.getLogger(__name__)


def _extract_json_from_response(response: Any) -> Dict[str, Any]:
    """
    Extract JSON data from an HTTP response.

    Args
    ----
    response : Any
        The HTTP response object.

    Returns
    -------
    Dict[str, Any]
        The parsed JSON data.

    Raises
    ------
    TokenRefreshJsonError
        If the response cannot be parsed as JSON.
    """
    # Try to use the client's json method first
    if hasattr(response, "json"):
        try:
            return cast(Dict[str, Any], response.json())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            raise TokenRefreshJsonError(f"Failed to decode token response: {e}") from e
        except Exception as e:
            if "json" in str(e).lower() or "decode" in str(e).lower():
                logger.error(f"Failed to decode JSON response: {e}")
                raise TokenRefreshJsonError(f"Failed to decode token response: {e}") from e
            raise

    # Fall back to manual JSON parsing
    if hasattr(response, "text"):
        try:
            return cast(Dict[str, Any], json.loads(response.text))
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            raise TokenRefreshJsonError(f"Failed to decode token response: {e}") from e

    if hasattr(response, "content"):
        try:
            return cast(Dict[str, Any], json.loads(response.content.decode("utf-8")))
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            raise TokenRefreshJsonError(f"Failed to decode token response: {e}") from e

    # No suitable content found
    raise TokenRefreshJsonError("Unable to extract response content")


def _check_http_status(response: Any) -> None:
    """
    Check if the HTTP response indicates an error.

    Args
    ----
    response : Any
        The HTTP response object.

    Raises
    ------
    TokenRefreshError
        If the response indicates an HTTP error.
    """
    if hasattr(response, "raise_for_status"):
        response.raise_for_status()
    elif hasattr(response, "status_code") and response.status_code >= 400:
        raise TokenRefreshError(f"HTTP error: {response.status_code}")


def _handle_exception(e: Exception) -> None:
    """
    Handle exceptions from HTTP requests and classify them appropriately.

    Args
    ----
    e : Exception
        The exception to handle.

    Raises
    ------
    TokenRefreshTimeoutError
        If the exception indicates a timeout.
    TokenRefreshNetworkError
        If the exception indicates a network error.
    TokenRefreshError
        For other errors.
    """
    error_type = type(e).__name__
    error_msg = str(e)

    # Handle timeout errors
    if "timeout" in error_type.lower() or "timeout" in error_msg.lower():
        logger.error(f"Token refresh request timed out: {e}")
        raise TokenRefreshTimeoutError(f"Token refresh request timed out: {e}") from e

    # Handle network errors
    if any(net_err in error_type.lower() for net_err in ["connect", "network", "connection"]):
        logger.error(f"Network error during token refresh: {e}")
        raise TokenRefreshNetworkError(f"Network error during token refresh: {e}") from e

    # Handle HTTP status errors
    if "status" in error_type.lower() or "http" in error_type.lower():
        logger.error(f"Token refresh request failed with HTTP error: {e}")
        raise TokenRefreshError(f"Token refresh failed with HTTP error: {e}") from e

    # Re-raise other errors
    logger.error(f"Unexpected error during token refresh: {e}")
    raise TokenRefreshError(f"Token refresh failed: {e}") from e


def _make_token_refresh_request(
    token_url: str,
    payload: Dict[str, Any],
    auth: Optional[Any] = None,
    timeout: float = 10.0,
    http_client: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Make the actual HTTP request to refresh the token.

    Args
    ----
    token_url : str
        The URL of the token endpoint.
    payload : Dict[str, Any]
        The request payload.
    auth : Optional[Any], optional
        Optional authentication to use with the request. Defaults to None.
    timeout : float, optional
        Request timeout in seconds. Defaults to 10.0.
    http_client : Optional[Any], optional
        Optional HTTP client instance to use for the request. Defaults to None.

    Returns
    -------
    Dict[str, Any]
        The parsed JSON response.

    Raises
    ------
    TokenRefreshTimeoutError
        If the request times out.
    TokenRefreshNetworkError
        If there's a network-related error.
    TokenRefreshJsonError
        If the response cannot be parsed as JSON.
    TokenRefreshError
        For other token refresh errors.

    Implementation Note
    -------------------
    This function requires an HTTP client (like httpx or requests) to make a POST
    request to the token_url. This client is not part of apiconfig's core dependencies.
    The actual HTTP request implementation should be provided by the consumer of this library.
    """
    if http_client is None:
        logger.error("No HTTP client provided for token refresh")
        raise TokenRefreshError("Token refresh requires an HTTP client. Please provide an HTTP client instance.")

    try:
        logger.debug(f"Making token refresh request to {token_url}")
        start_time = time.time()

        # Make the HTTP request using the provided client
        response = http_client.post(
            token_url,
            data=payload,
            auth=auth,
            timeout=timeout,
        )

        elapsed = time.time() - start_time
        logger.debug(f"Token refresh request completed in {elapsed:.2f}s")

        # Check for HTTP errors
        _check_http_status(response)

        # Parse the JSON response
        token_data = _extract_json_from_response(response)

        # Validate the response
        if "access_token" not in token_data:
            logger.error("Token response missing 'access_token'")
            raise TokenRefreshError("Refresh response missing 'access_token'")

        return token_data

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON response: {e}")
        raise TokenRefreshJsonError(f"Failed to decode token response: {e}") from e
    except TokenRefreshJsonError:
        # Re-raise JSON errors directly
        raise
    except Exception as e:
        # Handle other exceptions
        _handle_exception(e)
    # If we reach here, something went wrong; raise an error to satisfy the type checker
    raise TokenRefreshError("Token refresh failed: unexpected error in _make_token_refresh_request")


def _get_effective_settings(
    timeout: Optional[float],
    max_retries: Optional[int],
    client_config: Optional[ClientConfig],
) -> Tuple[float, int]:
    """
    Determine effective timeout and retry values from provided parameters or defaults.

    Args
    ----
    timeout : Optional[float]
        Explicit timeout value, if provided.
    max_retries : Optional[int]
        Explicit max retries value, if provided.
    client_config : Optional[ClientConfig]
        Optional client configuration to use for defaults.

    Returns
    -------
    Tuple[float, int]
        A tuple of (effective_timeout, effective_max_retries)
    """
    effective_timeout = timeout
    effective_max_retries = max_retries

    if client_config is not None:
        if effective_timeout is None:
            effective_timeout = client_config.timeout
        if effective_max_retries is None:
            effective_max_retries = client_config.retries

    # Use defaults if still None
    if effective_timeout is None:
        effective_timeout = 10.0
    if effective_max_retries is None:
        effective_max_retries = 3

    return effective_timeout, effective_max_retries


def _prepare_auth_and_payload(
    client_id: Optional[str],
    client_secret: Optional[str],
    refresh_token: str,
    extra_params: Optional[Dict[str, Any]],
    http_client: Optional[Any],
) -> Tuple[Optional[Any], Dict[str, Any]]:
    """
    Prepare authentication and payload for token refresh request.

    Args
    ----
    client_id : Optional[str]
        Optional client ID for authentication.
    client_secret : Optional[str]
        Optional client secret for authentication.
    refresh_token : str
        The refresh token to use.
    extra_params : Optional[Dict[str, Any]]
        Additional parameters to include in the payload.
    http_client : Optional[Any]
        The HTTP client to use for authentication.

    Returns
    -------
    Tuple[Optional[Any], Dict[str, Any]]
        A tuple of (auth, payload)
    """
    # Construct the request payload
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    if client_id:
        payload["client_id"] = client_id
    if client_secret:
        payload["client_secret"] = client_secret
    if extra_params:
        payload.update(extra_params)

    # Prepare authentication (if client_id/secret are provided and not in payload)
    auth = None
    if client_id and client_secret and http_client is not None:
        # Check if the HTTP client supports BasicAuth
        if hasattr(http_client, "BasicAuth"):
            # For httpx-like clients
            auth = http_client.BasicAuth(username=client_id, password=client_secret)
            # Remove from payload if using Basic Auth
            if "client_id" in payload:
                del payload["client_id"]
            if "client_secret" in payload:
                del payload["client_secret"]
        elif hasattr(http_client, "auth") and callable(http_client.auth):
            # For requests-like clients
            auth = (client_id, client_secret)
            # Remove from payload if using Basic Auth
            if "client_id" in payload:
                del payload["client_id"]
            if "client_secret" in payload:
                del payload["client_secret"]

    return auth, payload


def _execute_with_retry(
    token_url: str,
    payload: Dict[str, Any],
    auth: Optional[Any],
    timeout: float,
    max_retries: int,
    http_client: Optional[Any],
) -> Dict[str, Any]:
    """
    Execute token refresh request with retry logic.

    Args
    ----
    token_url : str
        The URL to send the request to.
    payload : Dict[str, Any]
        The request payload.
    auth : Optional[Any]
        Optional authentication to use.
    timeout : float
        Request timeout in seconds.
    max_retries : int
        Maximum number of retry attempts.
    http_client : Optional[Any]
        The HTTP client to use.

    Returns
    -------
    Dict[str, Any]
        The token data from a successful response.

    Raises
    ------
    TokenRefreshError
        If all retry attempts fail.
    """
    last_exception = None

    # Implement a simple retry mechanism
    for attempt in range(max_retries):
        try:
            # If not the first attempt, add exponential backoff
            if attempt > 0:
                backoff_time = min(2**attempt, 10)  # Exponential backoff with max of 10 seconds
                logger.debug(f"Retry attempt {attempt + 1}/{max_retries}, waiting {backoff_time}s")
                time.sleep(backoff_time)

            # Make the request
            token_data = _make_token_refresh_request(
                token_url=token_url,
                payload=payload,
                auth=auth,
                timeout=timeout,
                http_client=http_client,
            )

            # If successful, return the token data
            return token_data

        except (TokenRefreshNetworkError, TokenRefreshTimeoutError) as e:
            # These are retryable errors
            logger.warning(f"Retryable error during token refresh (attempt {attempt + 1}/{max_retries}): {e}")
            last_exception = e
            # Continue to the next retry attempt
            continue

        except Exception as e:
            # Non-retryable errors
            logger.error(f"Non-retryable error during token refresh: {e}")
            if isinstance(e, (TokenRefreshJsonError, TokenRefreshError)):
                raise
            else:
                raise TokenRefreshError(f"Token refresh failed: {e}") from e

    # If we've exhausted all retries, raise the last exception
    if last_exception:
        logger.error(f"Token refresh failed after {max_retries} attempts: {last_exception}")
        raise last_exception

    # This should never happen, but just in case
    raise TokenRefreshError(f"Token refresh failed after {max_retries} attempts")


def refresh_oauth2_token(
    refresh_token: str,
    token_url: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    extra_params: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    max_retries: Optional[int] = None,
    client_config: Optional[ClientConfig] = None,
    http_client: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Refresh an OAuth2 access token using a refresh token.

    This function handles the process of exchanging a refresh token for a new access token
    by making a POST request to the specified token URL. It includes logic for handling
    authentication, request payload construction, timeout, and retries for transient errors.

    Args
    ----
    refresh_token : str
        The refresh token to use for obtaining a new access token.
    token_url : str
        The URL of the OAuth2 token endpoint.
    client_id : Optional[str], optional
        The client ID for authentication, if required by the OAuth2 server. Defaults to None.
    client_secret : Optional[str], optional
        The client secret for authentication, if required by the OAuth2 server. Defaults to None.
    extra_params : Optional[Dict[str, Any]], optional
        Additional parameters to include in the token refresh request payload. Defaults to None.
    timeout : Optional[float], optional
        Request timeout in seconds. Overrides the timeout in `client_config` if provided. Defaults to None.
    max_retries : Optional[int], optional
        Maximum number of retry attempts for transient errors. Overrides the retries in `client_config` if provided. Defaults to None.
    client_config : Optional[ClientConfig], optional
        A ClientConfig instance to provide default timeout and retry settings. Defaults to None.
    http_client : Optional[Any], optional
        An instance of an HTTP client (e.g., `httpx.Client`, `requests.Session`) to use for the request.
        This client must support a `post` method with `url`, `data`, `auth`, and `timeout` parameters.
        Defaults to None.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the token data from the successful response, typically including
        'access_token', 'expires_in', 'token_type', and potentially a new 'refresh_token'.

    Raises
    ------
    TokenRefreshError
        If the token refresh process fails after all retry attempts, or for non-retryable errors
        such as invalid client credentials or server-side errors indicated by HTTP status codes.
    TokenRefreshTimeoutError
        If the request times out.
    TokenRefreshNetworkError
        If a network-related error occurs during the request.
    TokenRefreshJsonError
        If the response from the token endpoint cannot be parsed as JSON.
    """
    # Get effective timeout and retry settings
    effective_timeout, effective_max_retries = _get_effective_settings(timeout, max_retries, client_config)

    logger.debug(f"Token refresh using timeout={effective_timeout}s, max_retries={effective_max_retries}")

    # Prepare authentication and payload
    auth, payload = _prepare_auth_and_payload(client_id, client_secret, refresh_token, extra_params, http_client)

    # Execute the request with retry logic
    return _execute_with_retry(token_url, payload, auth, effective_timeout, effective_max_retries, http_client)
