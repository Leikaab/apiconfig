"""Tests for the FileProvider class."""

import json
import os
import pathlib
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

from apiconfig.config.providers.file import FileProvider
from apiconfig.exceptions.config import ConfigLoadError, ConfigValueError


class TestFileProvider:
    """Tests for the FileProvider class."""

    def test_init(self) -> None:
        """Test that FileProvider initializes correctly with string or Path."""
        # Test with string path
        provider1 = FileProvider(file_path="/path/to/config.json")
        assert isinstance(provider1.file_path, pathlib.Path)
        assert os.path.normpath(str(provider1.file_path)) == os.path.normpath("/path/to/config.json")

        # Test with Path object
        path_obj = Path("/path/to/config.json")
        provider2 = FileProvider(file_path=path_obj)
        assert os.path.normpath(str(provider2.file_path)) == os.path.normpath(str(path_obj))

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
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

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_load_non_dict_json(self) -> None:
        """Test loading a JSON file that doesn't contain a dictionary."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            # Write a JSON array instead of an object
            json.dump(["item1", "item2"], temp_file)
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            import re

            # Match the new error message with colon and normalized path
            expected_path = re.escape(os.path.normpath(temp_file.name))
            pattern = rf"must contain a JSON object: {expected_path}"
            with pytest.raises(ConfigLoadError, match=pattern):
                provider.load()

    def test_load_file_not_found(self) -> None:
        """Test loading a file that doesn't exist."""
        # Use a path that definitely doesn't exist
        import re

        non_existent_path = os.path.join("path", "that", "definitely", "does", "not", "exist", "config.json")
        provider = FileProvider(file_path=non_existent_path)

        # Accept both Windows and POSIX path separators in the error message
        escaped_path = re.escape(os.path.normpath(non_existent_path))
        pattern = rf"{escaped_path}.*not found|not found.*{escaped_path}"
        with pytest.raises(ConfigLoadError, match=pattern):
            provider.load()

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_load_invalid_json(self) -> None:
        """Test loading a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            # Write invalid JSON to the temp file
            temp_file.write('{"api": {"hostname": "example.com", invalid json}')
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            import re

            # Match the new error message with colon and normalized path
            expected_path = re.escape(os.path.normpath(temp_file.name))
            pattern = rf"Error decoding JSON in configuration file: {expected_path}"
            with pytest.raises(ConfigLoadError, match=pattern):
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

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_get_existing_value(self) -> None:
        """Test getting an existing configuration value."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            config_data = {
                "api": {"hostname": "example.com", "port": 443},
                "timeout": 30,
                "debug": True,
                "rate_limit": 100.5,
                "string_number": "42",
                "string_bool": "true",
            }
            json.dump(config_data, temp_file)
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            # Test getting top-level values
            assert provider.get("timeout") == 30
            assert provider.get("debug") is True
            assert provider.get("rate_limit") == 100.5

            # Test getting nested values with dot notation
            assert provider.get("api.hostname") == "example.com"
            assert provider.get("api.port") == 443

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_get_missing_value(self) -> None:
        """Test getting a missing configuration value."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            config_data = {"api": {"hostname": "example.com"}}
            json.dump(config_data, temp_file)
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            # Test with default value
            assert provider.get("missing", default="default_value") == "default_value"

            # Test without default value
            assert provider.get("missing") is None

            # Test missing nested value
            assert provider.get("api.missing") is None
            assert provider.get("api.missing", default=123) == 123

            # Test completely wrong path
            assert provider.get("not.a.valid.path") is None

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_get_with_type_coercion(self) -> None:
        """Test getting values with type coercion."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            config_data = {
                "string_int": "42",
                "string_float": "3.14",
                "string_bool_true": "true",
                "string_bool_false": "false",
                "number": 100,
                "decimal": 99.9,
            }
            json.dump(config_data, temp_file)
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            # String to int conversion
            int_value = provider.get("string_int", expected_type=int)
            assert int_value == 42
            assert isinstance(int_value, int)

            # String to float conversion
            float_value = provider.get("string_float", expected_type=float)
            assert float_value == 3.14
            assert isinstance(float_value, float)

            # String to bool conversion
            bool_true = provider.get("string_bool_true", expected_type=bool)
            assert bool_true is True
            bool_false = provider.get("string_bool_false", expected_type=bool)
            assert bool_false is False

            # Number to string conversion
            str_value = provider.get("number", expected_type=str)
            assert str_value == "100"
            assert isinstance(str_value, str)

            # Decimal to int conversion
            int_from_float = provider.get("decimal", expected_type=int)
            assert int_from_float == 99
            assert isinstance(int_from_float, int)

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_get_with_bool_variations(self) -> None:
        """Test boolean coercion with various string representations."""
        bool_variations: Dict[str, bool] = {
            "true": True,
            "True": True,
            "TRUE": True,
            "1": True,
            "yes": True,
            "Yes": True,
            "Y": True,
            "on": True,
            "false": False,
            "False": False,
            "FALSE": False,
            "0": False,
            "no": False,
            "No": False,
            "N": False,
            "off": False,
        }

        for string_value, expected_bool in bool_variations.items():
            with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
                config_data = {"bool_value": string_value}
                json.dump(config_data, temp_file)
                temp_file.flush()

                provider = FileProvider(file_path=temp_file.name)
                bool_value = provider.get("bool_value", expected_type=bool)
                assert bool_value is expected_bool, f"Failed for '{string_value}'"

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Known Windows compatibility issue")
    def test_get_invalid_type_coercion(self) -> None:
        """Test type coercion failures."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+") as temp_file:
            config_data = {
                "not_an_int": "abc",
                "not_a_float": "xyz",
                "not_a_bool": "maybe",
                "complex_value": {"nested": "value"},
            }
            json.dump(config_data, temp_file)
            temp_file.flush()

            provider = FileProvider(file_path=temp_file.name)

            # Invalid int conversion
            with pytest.raises(ConfigValueError, match="Cannot convert.*to int"):
                provider.get("not_an_int", expected_type=int)

            # Invalid float conversion
            with pytest.raises(ConfigValueError, match="Cannot convert.*to float"):
                provider.get("not_a_float", expected_type=float)

            # Invalid bool conversion
            with pytest.raises(ConfigValueError, match="Cannot convert.*to bool"):
                provider.get("not_a_bool", expected_type=bool)

            # Complex value to simple type
            with pytest.raises(ConfigValueError):
                provider.get("complex_value", expected_type=int)
