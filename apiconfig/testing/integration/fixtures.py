# apiconfig/testing/integration/fixtures.py
import json
from pathlib import Path
from typing import Any, Dict, Generator

import pytest

from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers.env import EnvironmentVariableProvider
from apiconfig.config.providers.file import FileProvider


@pytest.fixture(scope="function")
def temp_config_file(tmp_path: Path) -> Path:
    config_data: Dict[str, Any] = {
        "api": {"hostname": "file.example.com", "version": "v1"},
        "auth": {"type": "file_basic", "username": "file_user"},
    }
    config_file: Path = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture(scope="function")
def file_provider(temp_config_file: Path) -> FileProvider:
    return FileProvider(file_path=str(temp_config_file))


@pytest.fixture(scope="function")
def env_provider(monkeypatch: pytest.MonkeyPatch) -> EnvironmentVariableProvider:
    monkeypatch.setenv("APICONFIG_API_HOSTNAME", "env.example.com")
    monkeypatch.setenv("APICONFIG_AUTH_TYPE", "env_bearer")
    monkeypatch.setenv("APICONFIG_AUTH_TOKEN", "env_token_123")
    return EnvironmentVariableProvider(prefix="APICONFIG")


@pytest.fixture(scope="function")
def config_manager(
    file_provider: FileProvider, env_provider: EnvironmentVariableProvider
) -> ConfigManager:
    return ConfigManager(providers=[file_provider, env_provider])


@pytest.fixture(scope="session")
def mock_api_server() -> Generator[None, None, None]:
    # Placeholder for mock server setup and teardown
    # Implementation will be added in a future task
    yield
