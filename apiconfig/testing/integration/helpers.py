# apiconfig/testing/integration/helpers.py
import typing
import uuid

import httpx
from pytest_httpserver import HTTPServer  # type: ignore[import-untyped]

from apiconfig.auth.base import AuthStrategy
from apiconfig.config.base import ClientConfig
from apiconfig.config.manager import ConfigManager
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
) -> httpx.Response:
    """Internal implementation for make_request_with_config."""
    base_url = mock_server_url.rstrip("/")
    url = f"{base_url}/{path.lstrip('/')}"

    headers = kwargs.pop("headers", {})
    params = kwargs.pop("params", {})
    data = kwargs.pop("data", None)
    json_data = kwargs.pop("json", None)

    # Prepare request using auth strategy
    prepared_headers, prepared_params = auth_strategy.prepare_request(
        headers=headers, params=params
    )

    # Use httpx for the actual request
    # Use verify=False for self-signed certs often used by pytest-httpserver
    with httpx.Client(
        base_url=base_url,
        timeout=config.timeout,
        follow_redirects=True,  # Typically desired in tests
        verify=False,  # Add this for pytest-httpserver compatibility
    ) as client:
        response = client.request(
            method=method,
            url=url,
            headers=prepared_headers,
            params=prepared_params,
            data=data,
            json=json_data,
            **kwargs,
        )
    return response


def setup_multi_provider_manager(
    config_sources: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]]
) -> ConfigManager:
    """Internal implementation for setup_multi_provider_manager."""
    providers = []
    for name, data in config_sources:
        providers.append(MemoryProvider(data=data, name=name))
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
    """
    Configures the mock server to simulate a simple token endpoint.

    This is useful for testing custom authentication flows that involve
    fetching an access token (e.g., OAuth2 client credentials flow).

    Args:
        httpserver: The pytest-httpserver fixture instance.
        token_path: The path for the token endpoint.
        expected_body: The expected form-encoded body of the token request
                       (e.g., {'grant_type': 'client_credentials'}).
        access_token: The access token to return. If None, a random UUID is generated.
        token_type: The type of token (e.g., "Bearer").
        expires_in: The token expiry time in seconds.
        status_code: The HTTP status code for a successful token response.
        error_response: A dictionary representing the JSON error response if the
                        request body does not match `expected_body`.
        error_status_code: The HTTP status code for an error response.

    Returns:
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
        httpserver.expect_request(
            uri=token_path, method="POST"
        ).respond_with_json(error_resp_data, status=error_status_code)

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
