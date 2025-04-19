# apiconfig/testing/integration/helpers.pyi
import typing

import httpx
from pytest_httpserver import HTTPServer

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager

_T = typing.TypeVar("_T")


def make_request_with_config(
    config: ClientConfig,
    auth_strategy: AuthStrategy,
    mock_server_url: str,
    path: str,
    method: str = "GET",
    **kwargs: typing.Any,
) -> httpx.Response:
    """
    Makes an HTTP request using the provided config and auth strategy to a mock server.

    Handles applying authentication via the strategy's `prepare_request` method.

    Args:
        config: The ClientConfig instance.
        auth_strategy: The AuthStrategy instance.
        mock_server_url: The base URL of the mock server (from fixture).
        path: The request path.
        method: The HTTP method.
        **kwargs: Additional arguments passed to `httpx.Client.request`.

    Returns:
        The httpx.Response object.
    """
    ...


def setup_multi_provider_manager(
    config_sources: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]]
) -> ConfigManager:
    """
    Sets up a ConfigManager with multiple MemoryProviders for testing.

    Args:
        config_sources: A list of tuples, where each tuple contains a provider
                        name (str) and its configuration data (dict).

    Returns:
        A configured ConfigManager instance.
    """
    ...


def simulate_token_endpoint(
    httpserver: HTTPServer,
    token_path: str = "/oauth/token",
    expected_body: typing.Optional[typing.Dict[str, str]] = None,
    access_token: typing.Optional[str] = None,
    token_type: str = "Bearer",
    expires_in: int = 3600,
    status_code: int = 200,
    error_response: typing.Optional[typing.Dict[str, str]] = None,
    error_status_code: int = 400,
) -> str:
    """
    Configures the mock server to simulate a simple token endpoint.

    Useful for testing custom authentication flows involving token fetching.

    Args:
        httpserver: The pytest-httpserver fixture instance.
        token_path: The path for the token endpoint.
        expected_body: The expected form-encoded body of the token request.
        access_token: The access token to return. If None, a random UUID is generated.
        token_type: The type of token (e.g., "Bearer").
        expires_in: The token expiry time in seconds.
        status_code: The HTTP status code for a successful token response.
        error_response: JSON error response if the request body doesn't match.
        error_status_code: The HTTP status code for an error response.

    Returns:
        The access token string that the simulated endpoint will return.
    """
    ...
