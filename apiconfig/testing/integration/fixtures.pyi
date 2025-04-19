# apiconfig/testing/integration/fixtures.pyi
from pathlib import Path
from typing import Any, Generator

import pytest

from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.env import EnvProvider
from apiconfig.config.providers.file import FileProvider


@pytest.fixture(scope="function")
def temp_config_file(tmp_path: Path) -> Path:
    """
    Pytest fixture to create a temporary JSON configuration file.

    Args:
        tmp_path: Pytest's built-in fixture for temporary directories.

    Returns:
        The Path object pointing to the created temporary config file.
    """
    ...


@pytest.fixture(scope="function")
def file_provider(temp_config_file: Path) -> FileProvider:
    """
    Pytest fixture to create a FileProvider instance using a temporary config file.

    Args:
        temp_config_file: The fixture providing the path to the temporary config file.

    Returns:
        An initialized FileProvider instance.
    """
    ...


@pytest.fixture(scope="function")
def env_provider(monkeypatch: pytest.MonkeyPatch) -> EnvProvider:
    """
    Pytest fixture to create an EnvProvider instance with mocked env vars.

    Sets environment variables like APICONFIG_API_HOSTNAME, APICONFIG_AUTH_TYPE, etc.

    Args:
        monkeypatch: Pytest's fixture for modifying environment variables.

    Returns:
        An initialized EnvProvider instance.
    """
    ...


@pytest.fixture(scope="function")
def config_manager(
    file_provider: FileProvider, env_provider: EnvProvider
) -> ConfigManager:
    """
    Pytest fixture to create a ConfigManager instance with file and env providers.

    Args:
        file_provider: The fixture providing the FileProvider.
        env_provider: The fixture providing the EnvProvider.

    Returns:
        An initialized ConfigManager instance.
    """
    ...


@pytest.fixture(scope="session")
def mock_api_server() -> Generator[None, None, None]:
    """
    Pytest fixture placeholder for a mock HTTP API server.

    This fixture is intended for integration tests that require simulating
    API responses. The actual server implementation (e.g., using aiohttp or
    another library) will be added in a separate task.

    Yields:
        None. The fixture manages the lifecycle of the mock server.
    """
    ...
