# -*- coding: utf-8 -*-
"""Helper functions for integration tests."""

# apiconfig/testing/integration/helpers.py
import typing
import uuid

from httpx import Client, Response
from pytest_httpserver import HTTPServer

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager, ConfigProvider
from apiconfig.config.providers.memory import MemoryProvider
from apiconfig.testing.integration.servers import configure_mock_response

_T = typing.TypeVar("_T")


def make_request_with_config(
    config: ClientConfig,
    auth_strategy: AuthStrategy,
    mock_server_url: str,
    path: str,
    method: str = "GET",
    **kwargs: typing.Any,
) -> Response:
    """Make an HTTP request using the provided config and auth strategy to a mock server.

    Handles applying authentication via the strategy's `prepare_request` method.

    Args
    ----
    config : ClientConfig
        The ClientConfig instance.
    auth_strategy : AuthStrategy
        The AuthStrategy instance.
    mock_server_url : str
        The base URL of the mock server (from fixture).
    path : str
        The request path.
    method : str, optional
        The HTTP method.
    **kwargs : Any
        Additional arguments passed to `Client.request`.

    Returns
    -------
    Response
        The httpx Response object.
    """
    base_url = mock_server_url.rstrip("/")
    url = f"{base_url}/{path.lstrip('/')}"

    headers = kwargs.pop("headers", {})
    params = kwargs.pop("params", {})
    data = kwargs.pop("data", None)
    json_data = kwargs.pop("json", None)

    # Prepare request using auth strategy
    prepared_headers = auth_strategy.prepare_request_headers()
    prepared_params = auth_strategy.prepare_request_params()

    # Merge any user-supplied headers/params (user takes precedence)
    prepared_headers.update(headers)

    # Convert prepared_params to dict and merge with user params
    safe_params = dict(prepared_params) if prepared_params else {}
    safe_params.update(params)

    # Ensure headers are always dicts (not mocks)
    safe_headers = dict(prepared_headers)

    # Use httpx's Client for the actual request
    # Use verify=False for self-signed certs often used by pytest-httpserver
    with Client(
        base_url=base_url,
        timeout=config.timeout,
        follow_redirects=True,  # Typically desired in tests
        verify=False,  # Add this for pytest-httpserver compatibility
    ) as client:
        response = client.request(
            method=method,
            url=url,
            headers=safe_headers,
            params=safe_params,
            data=data,
            json=json_data,
            **kwargs,
        )
    return response


def setup_multi_provider_manager(
    config_sources: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]],
) -> ConfigManager:
    """Set up a ConfigManager with multiple MemoryProviders for testing.

    Args
    ----
    config_sources : list[tuple[str, dict[str, Any]]]
        A list of tuples, where each tuple contains a provider
        name (str) and its configuration data (dict).

    Returns
    -------
    ConfigManager
        A configured ConfigManager instance.
    """
    providers: list[ConfigProvider] = []
    for name, data in config_sources:
        providers.append(MemoryProvider(config_data=data))
        # Store name as an attribute for testing
        providers[-1].name = name  # type: ignore[union-attr]
    return ConfigManager(providers=providers)


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
    """Configure the mock server to simulate a simple token endpoint.

    Useful for testing custom authentication flows involving token fetching.

    Args
    ----
    httpserver : HTTPServer
        The pytest-httpserver fixture instance.
    token_path : str, optional
        The path for the token endpoint.
    expected_body : dict[str, str] | None, optional
        The expected form-encoded body of the token request.
    access_token : str | None, optional
        The access token to return. If None, a random UUID is generated.
    token_type : str, optional
        The type of token (e.g., "Bearer").
    expires_in : int, optional
        The token expiry time in seconds.
    status_code : int, optional
        The HTTP status code for a successful token response.
    error_response : dict[str, str] | None, optional
        JSON error response if the request body doesn't match.
    error_status_code : int, optional
        The HTTP status code for an error response.

    Returns
    -------
    str
        The access token string that the simulated endpoint will return.
    """
    if access_token is None:
        access_token = str(uuid.uuid4())

    success_response = {
        "access_token": access_token,
        "token_type": token_type,
        "expires_in": expires_in,
    }

    if expected_body:
        # Convert dict to form-encoded string for matching
        expected_data_str = "&".join(f"{k}={v}" for k, v in expected_body.items())

        # Configure error response if body doesn't match
        error_resp_data = error_response or {"error": "invalid_request"}
        httpserver.expect_request(uri=token_path, method="POST").respond_with_json(error_resp_data, status=error_status_code)

        # Configure success response for matching body
        configure_mock_response(
            httpserver=httpserver,
            path=token_path,
            method="POST",
            match_data=expected_data_str,  # Match form-encoded data
            match_headers={"Content-Type": "application/x-www-form-urlencoded"},
            response_data=success_response,
            status_code=status_code,
            ordered=True,  # Ensure this matches before the generic error
        )
    else:
        # Configure success response without body matching
        configure_mock_response(
            httpserver=httpserver,
            path=token_path,
            method="POST",
            response_data=success_response,
            status_code=status_code,
        )

    return access_token
