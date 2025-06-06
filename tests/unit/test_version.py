import importlib
import importlib.metadata


class TestVersion:
    """Tests for package version handling."""

    def test_version_defaults_to_zero_when_package_missing(self, monkeypatch) -> None:
        """__version__ should fallback to '0.0.0' when package metadata is missing."""

        def raise_package_not_found(_name: str) -> str:
            raise importlib.metadata.PackageNotFoundError

        monkeypatch.setattr(importlib.metadata, "version", raise_package_not_found)

        module = importlib.reload(importlib.import_module("apiconfig"))
        assert module.__version__ == "0.0.0"
