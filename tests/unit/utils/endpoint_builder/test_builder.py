"""
Unit tests for endpoint_builder builder module.
"""

from unittest.mock import Mock

from apiconfig.utils.endpoint_builder.builder import EndpointBuilder


class TestEndpointBuilder:
    """Test the EndpointBuilder class."""

    def test_init_minimal(self) -> None:
        """Test EndpointBuilder initialization with minimal arguments."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder()
        assert builder.resource_path == "items"
        assert builder.parent_builder is None
        assert builder.endpoint_prefix is None

    def test_init_with_parent(self) -> None:
        """Test EndpointBuilder initialization with a parent builder."""
        parent_builder = Mock()

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder(parent_builder=parent_builder)
        assert builder.resource_path == "items"
        assert builder.parent_builder == parent_builder
        assert builder.endpoint_prefix is None

    def test_init_with_endpoint_prefix(self) -> None:
        """Test EndpointBuilder initialization with endpoint prefix."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"
            endpoint_prefix = ["/api/v1"]

        builder = TestBuilder()
        assert builder.resource_path == "items"
        assert builder.parent_builder is None
        assert builder.endpoint_prefix == ["/api/v1"]

    def test_build_endpoint_simple(self) -> None:
        """Test building a simple endpoint without args."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder()
        endpoint = builder.build_endpoint()
        assert endpoint == "items"

    def test_build_endpoint_with_id(self) -> None:
        """Test building an endpoint with a resource ID."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder()
        endpoint = builder.build_endpoint(123)
        assert endpoint == "items/123"

    def test_build_endpoint_with_multiple_args(self) -> None:
        """Test building an endpoint with multiple arguments."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder()
        endpoint = builder.build_endpoint(123, "details", "info")
        assert endpoint == "items/123/details/info"

    def test_build_endpoint_with_parent(self) -> None:
        """Test building an endpoint with a parent builder."""
        parent_builder = Mock()
        parent_builder.resource_path = "users"
        parent_builder.parent_builder = None
        parent_builder.get_parent_path.return_value = None
        parent_builder.get_prefix_segments.return_value = []
        parent_builder.build_endpoint.return_value = "/users/123"
        parent_builder._get_endpoint_prefix.return_value = None

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        child_builder = TestBuilder(parent_builder=parent_builder)
        endpoint = child_builder.build_endpoint(456, parent_args=[123])
        assert endpoint == "users/123/items/456"

    def test_build_endpoint_with_nested_parents(self) -> None:
        """Test building an endpoint with nested parent builders."""
        grandparent_builder = Mock()
        grandparent_builder.resource_path = "organizations"
        grandparent_builder.parent_builder = None
        grandparent_builder.get_parent_path.return_value = None
        grandparent_builder.get_prefix_segments.return_value = []
        grandparent_builder.build_endpoint.return_value = "/organizations/1"
        grandparent_builder._get_endpoint_prefix.return_value = None

        parent_builder = Mock()
        parent_builder.resource_path = "users"
        parent_builder.parent_builder = grandparent_builder
        parent_builder.get_parent_path.return_value = "/organizations/1"
        parent_builder.get_prefix_segments.return_value = []
        parent_builder.build_endpoint.return_value = "/organizations/1/users/123"
        parent_builder._get_endpoint_prefix.return_value = None

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        child_builder = TestBuilder(parent_builder=parent_builder)
        endpoint = child_builder.build_endpoint(456, parent_args=[123, 1])
        assert endpoint == "organizations/1/users/123/items/456"

    def test_build_endpoint_with_prefix(self) -> None:
        """Test building an endpoint with endpoint prefix."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"
            endpoint_prefix = ["api", "v2"]

        builder = TestBuilder()
        endpoint = builder.build_endpoint(123)
        assert endpoint == "api/v2/items/123"

    def test_get_parent_path_no_parent(self) -> None:
        """Test get_parent_path with no parent builder."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder()
        assert builder.get_parent_path() is None

    def test_get_parent_path_with_parent(self) -> None:
        """Test get_parent_path with a parent builder."""
        parent_builder = Mock()
        parent_builder.resource_path = "users"
        parent_builder.parent_builder = None
        parent_builder.get_parent_path.return_value = None
        parent_builder.get_prefix_segments.return_value = []
        parent_builder.build_endpoint.return_value = "/users/123"
        parent_builder._get_endpoint_prefix.return_value = None

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        child_builder = TestBuilder(parent_builder=parent_builder)
        parent_path = child_builder.get_parent_path([123])
        assert parent_path == "/users/123"

    def test_get_prefix_segments_no_prefix(self) -> None:
        """Test get_prefix_segments with no endpoint prefix."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"

        builder = TestBuilder()
        segments = builder.get_prefix_segments()
        assert segments == []

    def test_get_prefix_segments_with_prefix(self) -> None:
        """Test get_prefix_segments with endpoint prefix."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"
            endpoint_prefix = ["api", "v1"]

        builder = TestBuilder()
        segments = builder.get_prefix_segments()
        assert segments == ["api", "v1"]

    def test_get_prefix_segments_with_empty_prefix(self) -> None:
        """Test get_prefix_segments with empty endpoint prefix."""

        class TestBuilder(EndpointBuilder):
            resource_path = "items"
            endpoint_prefix = []

        builder = TestBuilder()
        segments = builder.get_prefix_segments()
        assert segments == []


class TestEndpointBuilderNestedPrefix:
    """Test how prefixes combine with real (non-mock) parent builders."""

    def test_parent_prefix_is_not_repeated_for_child(self) -> None:
        """A child placed under its parent path gets the parent's prefix only once."""

        class ParentBuilder(EndpointBuilder):
            resource_path = "companies"
            endpoint_prefix = ["api"]

        class ChildBuilder(EndpointBuilder):
            resource_path = "contacts"

        child = ChildBuilder(parent_builder=ParentBuilder())
        assert child.build_endpoint(1, parent_args=["acme"]) == "api/companies/acme/contacts/1"
        assert child.build_endpoint() == "api/companies/contacts"

    def test_append_mode_child_under_parent_path(self) -> None:
        """An append-mode child does not duplicate the parent prefix in front of the parent path."""

        class ParentBuilder(EndpointBuilder):
            resource_path = "companies"
            endpoint_prefix = ["api"]

        class ChildBuilder(EndpointBuilder):
            resource_path = "contacts"
            endpoint_prefix = ["x"]
            prefix_mode = "append"

        child = ChildBuilder(parent_builder=ParentBuilder())
        assert child.build_endpoint(1, parent_args=["acme"]) == "api/companies/acme/contacts/1"

    def test_prefix_used_without_parent(self) -> None:
        """A resource without a parent gets its own prefix."""

        class Builder(EndpointBuilder):
            resource_path = "contacts"
            endpoint_prefix = "companies/acme"

        assert Builder().build_endpoint(1) == "companies/acme/contacts/1"

    def test_none_and_empty_segments_are_skipped(self) -> None:
        """None and empty segments are accepted and left out of the path."""

        class Builder(EndpointBuilder):
            resource_path = "items"

        assert Builder().build_endpoint(1, None, "", "details") == "items/1/details"
