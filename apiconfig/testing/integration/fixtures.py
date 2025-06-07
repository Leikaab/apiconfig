# -*- coding: utf-8 -*-
"""Pytest fixtures for integration tests."""

# apiconfig/testing/integration/fixtures.py
import json
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import pytest
from pytest_httpserver import HTTPServer

from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.env import EnvProvider  # Corrected import
from apiconfig.config.providers.file import FileProvider

# Type alias for the custom auth callable used in tests
CustomAuthCallable = Callable[[Dict[str, str], Dict[str, str]], tuple[Dict[str, str], Dict[str, str]]]


@pytest.fixture(scope="session")
def httpserver_listen_address() -> tuple[str, int]:
    """Configure listen address for the HTTPServer fixture."""
    # Listen on loopback, random available port. Session scope is efficient.
    return ("127.0.0.1", 0)


# Note: pytest-httpserver automatically provides the 'httpserver' fixture
# if pytest-httpserver is installed and the listen address fixture is defined.


@pytest.fixture(scope="function")
def mock_api_url(httpserver: HTTPServer) -> str:
    """Provide the base URL of the running mock API server."""
    # Ensures trailing slash for easy joining with paths
    return str(httpserver.url_for("/"))


@pytest.fixture(scope="function")
def temp_config_file(tmp_path: Path) -> Path:
    """Create a temporary JSON config file for testing."""
    config_data: Dict[str, Any] = {
        "api": {
            "hostname": "file.example.com",
            "version": "v1",
        },  # Hostname usually overridden by mock_api_url in tests
        "auth": {"type": "file_basic", "username": "file_user"},
    }
    config_file: Path = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture(scope="function")
def file_provider(temp_config_file: Path) -> FileProvider:
    """Provide a FileProvider instance pointing to a temporary config file."""
    return FileProvider(file_path=str(temp_config_file))


@pytest.fixture(scope="function")
def env_provider(monkeypatch: pytest.MonkeyPatch) -> EnvProvider:
    """Provide an EnvProvider with predefined environment variables."""
    monkeypatch.setenv("APICONFIG_API_HOSTNAME", "env.example.com")  # Hostname usually overridden by mock_api_url in tests
    monkeypatch.setenv("APICONFIG_AUTH_TYPE", "env_bearer")
    monkeypatch.setenv("APICONFIG_AUTH_TOKEN", "env_token_123")
    return EnvProvider(prefix="APICONFIG")


@pytest.fixture(scope="function")
def config_manager(file_provider: FileProvider, env_provider: EnvProvider) -> ConfigManager:
    """Provide a ConfigManager instance with file and env providers."""
    # Order matters: env overrides file by default
    return ConfigManager(providers=[file_provider, env_provider])


@pytest.fixture(scope="function")
def custom_auth_strategy_factory() -> Callable[[Optional[CustomAuthCallable]], CustomAuth]:
    """Provide a factory fixture to create CustomAuth instances for testing.

    This allows tests to easily define and inject specific custom authentication
    logic via a callable.

    The factory takes an optional callable (`auth_callable`) which implements the
    custom authentication logic. The callable must accept two dictionaries
    (headers, params) and return a tuple containing the potentially modified
    headers and params dictionaries.

    If no callable is provided, a default no-op callable is used.

    Returns
    -------
    Callable[[Optional[CustomAuthCallable]], CustomAuth]
        A factory function that creates CustomAuth instances.

    Example Usage in a test
    -----------------------
    ```python
    def test_custom_header_auth(custom_auth_strategy_factory, httpserver, mock_api_url):
        # Define the custom logic
        def add_custom_header(headers, params):
            headers['X-Custom-API-Key'] = 'secret-test-key'
            return headers, params

        # Create the strategy using the factory
        auth_strategy = custom_auth_strategy_factory(add_custom_header)

        # Configure the mock server to expect the header
        configure_mock_response(
            httpserver, "/test", match_headers={'X-Custom-API-Key': 'secret-test-key'}
        )

        # Make a request using a client configured with this strategy...
        # Assert the request was received correctly using assert_request_received...
    ```
    """

    def _factory(auth_callable: Optional[CustomAuthCallable] = None) -> CustomAuth:
        """Create a CustomAuth instance with the given callable.

        If a callable is provided, it will be used to modify headers and params.
        The callable must accept (headers, params) and return (headers, params).
        The CustomAuth strategy expects header_callback and param_callback that
        return only headers or params, so we wrap the provided callable accordingly.
        """
        if auth_callable is None:
            # Default no-op callable if none provided
            def default_callable(headers: Dict[str, str], params: Dict[str, str]) -> tuple[Dict[str, str], Dict[str, str]]:
                # Simply return the inputs unmodified
                return headers, params

            auth_callable = default_callable

        def header_callback() -> Dict[str, str]:
            headers, _ = auth_callable({}, {})
            return headers

        def param_callback() -> Dict[str, str]:
            _, params = auth_callable({}, {})
            return params

        # At least one callback must be provided, so we provide both
        return CustomAuth(header_callback=header_callback, param_callback=param_callback)

    return _factory
