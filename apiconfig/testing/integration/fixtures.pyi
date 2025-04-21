# apiconfig/testing/integration/fixtures.pyi
import json
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Optional

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_httpserver import HTTPServer

from apiconfig.auth.strategies.custom import CustomAuth
from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.env import EnvProvider
from apiconfig.config.providers.file import FileProvider

# Type alias for the custom auth callable used in tests
CustomAuthCallable = Callable[[Dict[str, str], Dict[str, str]], tuple[Dict[str, str], Dict[str, str]]]

@pytest.fixture(scope="session")
def httpserver_listen_address() -> tuple[str, int]:
    """Configure listen address for the HTTPServer fixture."""
    ...

# Note: pytest-httpserver automatically provides the 'httpserver' fixture

@pytest.fixture(scope="function")
def mock_api_url(httpserver: HTTPServer) -> str:
    """Provides the base URL of the running mock API server."""
    ...

@pytest.fixture(scope="function")
def temp_config_file(tmp_path: Path) -> Path:
    """Creates a temporary JSON config file for testing."""
    ...

@pytest.fixture(scope="function")
def file_provider(temp_config_file: Path) -> FileProvider:
    """Provides a FileProvider instance pointing to a temporary config file."""
    ...

@pytest.fixture(scope="function")
def env_provider(monkeypatch: MonkeyPatch) -> EnvProvider:
    """Provides an EnvProvider with predefined env vars."""
    ...

@pytest.fixture(scope="function")
def config_manager(file_provider: FileProvider, env_provider: EnvProvider) -> ConfigManager:
    """Provides a ConfigManager instance with file and env providers."""
    ...

@pytest.fixture(scope="function")
def custom_auth_strategy_factory() -> Callable[[Optional[CustomAuthCallable]], CustomAuth]:
    """
    Provides a factory fixture to create CustomAuth instances for testing.

    Allows tests to inject specific custom authentication logic via a callable.
    The factory takes an optional callable (`auth_callable`) which accepts
    headers and params dicts and returns modified versions.

    Returns:
        A factory function that creates CustomAuth instances.

    Example Usage: See .py file docstring.
    """
    ...
