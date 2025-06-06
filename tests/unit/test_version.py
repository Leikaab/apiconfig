import importlib
import importlib.metadata

import pytest


class TestVersion:
    """Tests for package version handling."""

    def test_version_defaults_to_zero_when_package_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """__version__ should fallback to '0.0.0' when package metadata is missing."""

        def raise_package_not_found(_name: str) -> str:
            raise importlib.metadata.PackageNotFoundError

        monkeypatch.setattr(importlib.metadata, "version", raise_package_not_found)

        module = importlib.reload(importlib.import_module("apiconfig"))
        assert module.__version__ == "0.0.0"

    def test_version_uses_metadata_when_available(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """__version__ should use the value from package metadata when available."""

        monkeypatch.setattr(importlib.metadata, "version", lambda _name: "1.2.3")

        module = importlib.reload(importlib.import_module("apiconfig"))
        assert module.__version__ == "1.2.3"
