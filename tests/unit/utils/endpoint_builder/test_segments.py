"""
Unit tests for endpoint_builder segments module.
"""

from apiconfig.utils.endpoint_builder.segments import build_resource_segments


class TestBuildResourceSegments:
    """Test the build_resource_segments function."""

    def test_build_resource_segments_basic(self) -> None:
        """Test basic resource segment building."""
        result = build_resource_segments("users", 123, "posts")
        assert result == ["users", "123", "posts"]

    def test_build_resource_segments_no_resource_path(self) -> None:
        """Test building segments without a resource path."""
        result = build_resource_segments(None, "posts", 456)
        assert result == ["posts", "456"]

    def test_build_resource_segments_empty_resource_path(self) -> None:
        """Test building segments with empty resource path."""
        result = build_resource_segments("", "posts", 456)
        assert result == ["posts", "456"]

    def test_build_resource_segments_no_args(self) -> None:
        """Test building segments with only resource path."""
        result = build_resource_segments("users")
        assert result == ["users"]

    def test_build_resource_segments_no_path_no_args(self) -> None:
        """Test building segments with no path and no args."""
        result = build_resource_segments(None)
        assert result == []

    def test_build_resource_segments_with_none_args(self) -> None:
        """Test building segments with None values in args."""
        result = build_resource_segments("users", 123, None, "posts", None)
        assert result == ["users", "123", "posts"]

    def test_build_resource_segments_all_none(self) -> None:
        """Test building segments with all None values."""
        result = build_resource_segments(None, None, None)
        assert result == []

    def test_build_resource_segments_integers(self) -> None:
        """Test building segments with integer arguments."""
        result = build_resource_segments("users", 123, 456, 789)
        assert result == ["users", "123", "456", "789"]

    def test_build_resource_segments_mixed_types(self) -> None:
        """Test building segments with mixed types."""
        result = build_resource_segments("api", "v1", 2, "users", 100)
        assert result == ["api", "v1", "2", "users", "100"]

    def test_build_resource_segments_zero(self) -> None:
        """Test building segments with zero."""
        result = build_resource_segments("users", 0, "posts")
        assert result == ["users", "0", "posts"]

    def test_build_resource_segments_string_numbers(self) -> None:
        """Test building segments with string numbers."""
        result = build_resource_segments("users", "123", "posts", "456")
        assert result == ["users", "123", "posts", "456"]

    def test_build_resource_segments_single_arg(self) -> None:
        """Test building segments with single additional arg."""
        result = build_resource_segments("users", 123)
        assert result == ["users", "123"]

    def test_build_resource_segments_many_args(self) -> None:
        """Test building segments with many args."""
        result = build_resource_segments("api", "v1", "users", 123, "posts", 456, "comments")
        assert result == ["api", "v1", "users", "123", "posts", "456", "comments"]

    def test_build_resource_segments_empty_strings_in_args(self) -> None:
        """Test that empty strings in args are included (not filtered out)."""
        # This matches the original behavior where only None is filtered
        result = build_resource_segments("users", "", "posts")
        assert result == ["users", "", "posts"]

    def test_build_resource_segments_whitespace_strings(self) -> None:
        """Test that whitespace strings are included as-is."""
        result = build_resource_segments("users", "  ", "posts")
        assert result == ["users", "  ", "posts"]
