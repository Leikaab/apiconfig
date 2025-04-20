"""Tests for the auth/token/__init__.py module."""

from apiconfig.auth.token import (
    __all__,
)


class TestTokenInit:
    """Tests for the auth/token/__init__.py module."""

    def test_all_exports(self) -> None:
        """Test that __all__ contains the expected exports."""
        expected_exports = [
            "TokenStorage",
            "InMemoryTokenStorage",
            "refresh_oauth2_token",
        ]

        # Check that __all__ contains all expected exports
        for export in expected_exports:
            assert export in __all__

        # Check that __all__ doesn't contain any unexpected exports
        assert len(__all__) == len(expected_exports)

        # Check that all exports are importable from the module
        import apiconfig.auth.token
        module_globals = dir(apiconfig.auth.token)
        for export in __all__:
            assert export in module_globals
