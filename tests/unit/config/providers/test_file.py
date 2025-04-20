"""Tests for the FileProvider class."""

import json
import pathlib
import tempfile
from pathlib import Path
from typing import Any


import pytest

import pytest

from apiconfig.config.providers.file import FileProvider
from apiconfig.exceptions.config import ConfigLoadError


class TestFileProvider:
    """Tests for the FileProvider class."""

    def test_init(self) -> None:
        """Test that FileProvider initializes correctly with string or Path."""
        # Test with string path
        provider1 = FileProvider(file_path="/path/to/config.json")
        assert isinstance(provider1._file_path, pathlib.Path)
        assert str(provider1._file_path) == "/path/to/config.json"

        # Test with Path object
        path_obj = Path("/path/to/config.json")
        provider2 = FileProvider(file_path=path_obj)
        assert provider2._file_path == path_obj

    def test_load_valid_json(self) -> None:
        """Test loading a valid JSON file."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            # Write valid JSON to the temp file
            config_data = {"api": {"hostname": "example.com"}, "timeout": 30}
            json.dump(config_data, temp_file)
            temp_file.flush()

            # Create provider and load the config
            provider = FileProvider(file_path=temp_file.name)
            loaded_config = provider.load()

            # Check that the loaded config matches the original
            assert loaded_config == config_data
            assert loaded_config["api"]["hostname"] == "example.com"
            assert loaded_config["timeout"] == 30

    def test_load_unsupported_file_type(self) -> None:
        """Test loading a file with an unsupported extension."""
        with tempfile.NamedTemporaryFile(suffix=".yaml") as temp_file:
            provider = FileProvider(file_path=temp_file.name)

            with pytest.raises(ConfigLoadError, match="Unsupported file type"):
                provider.load()

    def test_load_non_dict_json(self) -> None:
        """Test loading a JSON file that doesn't contain a dictionary."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            # Write a JSON array instead of an object
            json.dump(["item1", "item2"], temp_file)
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            with pytest.raises(ConfigLoadError, match="must contain a JSON object"):
                provider.load()

    def test_load_file_not_found(self) -> None:
        """Test loading a file that doesn't exist."""
        # Use a path that definitely doesn't exist
        non_existent_path = "/path/that/definitely/does/not/exist/config.json"
        provider = FileProvider(file_path=non_existent_path)

        with pytest.raises(ConfigLoadError, match="not found"):
            provider.load()

    def test_load_invalid_json(self) -> None:
        """Test loading a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            # Write invalid JSON to the temp file
            temp_file.write('{"api": {"hostname": "example.com", invalid json}')
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            with pytest.raises(ConfigLoadError, match="Error decoding JSON"):
                provider.load()

    def test_load_permission_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading a file with insufficient permissions."""
        with tempfile.NamedTemporaryFile(suffix=".json") as temp_file:
            # Mock pathlib.Path.open to raise PermissionError
            def mock_open(*args: Any, **kwargs: Any) -> None:
                raise PermissionError("Permission denied")

            monkeypatch.setattr(pathlib.Path, "open", mock_open)

            provider = FileProvider(file_path=temp_file.name)

            with pytest.raises(ConfigLoadError, match="Error reading configuration file"):
                provider.load()

    def test_load_other_os_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading a file with other OS errors."""
        with tempfile.NamedTemporaryFile(suffix=".json") as temp_file:
            # Mock pathlib.Path.open to raise OSError
            def mock_open(*args: Any, **kwargs: Any) -> None:
                raise OSError("Some other OS error")

            monkeypatch.setattr(pathlib.Path, "open", mock_open)

            provider = FileProvider(file_path=temp_file.name)

            with pytest.raises(ConfigLoadError, match="Error reading configuration file"):
                provider.load()
