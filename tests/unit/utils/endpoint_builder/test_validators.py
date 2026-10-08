"""
Unit tests for endpoint_builder validators module.
"""

import pytest

from apiconfig.utils.endpoint_builder.validators import validate_path_segments


class TestValidatePathSegments:
    """Test the validate_path_segments function."""

    def test_validate_path_segments_valid(self) -> None:
        """Test validation passes for valid path segments."""
        # Should not raise any exceptions
        validate_path_segments("users", 123, "posts")
        validate_path_segments("users")
        validate_path_segments()

    def test_validate_path_segments_numeric(self) -> None:
        """Test validation passes for numeric values."""
        validate_path_segments(123, 456)
        validate_path_segments("users", 999)

    def test_validate_path_segments_none(self) -> None:
        """Test validation accepts None values, which are skipped when joining."""
        validate_path_segments("users", None, "posts")

    def test_validate_path_segments_empty_string(self) -> None:
        """Test validation accepts empty strings, which are skipped when joining."""
        validate_path_segments("users", "", "posts")
        validate_path_segments("   ")  # Whitespace only

    def test_validate_path_segments_invalid_type(self) -> None:
        """Test validation fails for invalid types."""
        with pytest.raises(TypeError, match="Path segment must be string or integer"):
            validate_path_segments("users", [], "posts")  # type: ignore[arg-type]

        with pytest.raises(TypeError, match="Path segment must be string or integer"):
            validate_path_segments({"key": "value"})  # type: ignore[arg-type]

    def test_validate_path_segments_dangerous_chars(self) -> None:
        """Test validation fails for dangerous characters."""
        with pytest.raises(ValueError, match="Path segment contains potentially dangerous characters"):
            validate_path_segments("users", "../etc/passwd")

        with pytest.raises(ValueError, match="Path segment contains potentially dangerous characters"):
            validate_path_segments("/absolute/path")

        with pytest.raises(ValueError, match="Path segment contains potentially dangerous characters"):
            validate_path_segments("trailing/")

    def test_validate_path_segments_mixed_valid_invalid(self) -> None:
        """Test validation with mixed valid and invalid segments."""
        with pytest.raises(ValueError, match="Path segment contains potentially dangerous characters"):
            validate_path_segments("users", 123, None, "../posts")
