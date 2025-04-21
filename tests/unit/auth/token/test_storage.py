import pytest

from apiconfig.auth.token.storage import InMemoryTokenStorage, TokenStorage


class TestTokenStorage:
    """Tests for the TokenStorage abstract base class."""

    def test_token_storage_is_abstract(self) -> None:
        """Test that TokenStorage is an abstract base class that cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            TokenStorage()  # type: ignore

    def test_token_storage_abstract_methods(self) -> None:
        """Test that TokenStorage defines the expected abstract methods."""
        abstract_methods = TokenStorage.__abstractmethods__
        assert "store_token" in abstract_methods
        assert "retrieve_token" in abstract_methods
        assert "delete_token" in abstract_methods


class TestInMemoryTokenStorage:
    """Tests for the InMemoryTokenStorage implementation."""

    def test_init(self) -> None:
        """Test that InMemoryTokenStorage initializes with an empty storage dict."""
        storage = InMemoryTokenStorage()
        assert storage._storage == {}

    def test_store_token(self) -> None:
        """Test storing a token."""
        storage = InMemoryTokenStorage()
        storage.store_token("test_key", "test_token")
        assert storage._storage["test_key"] == "test_token"

        # Test overwriting an existing token
        storage.store_token("test_key", "new_token")
        assert storage._storage["test_key"] == "new_token"

    def test_retrieve_token(self) -> None:
        """Test retrieving a token."""
        storage = InMemoryTokenStorage()

        # Test retrieving a non-existent token
        assert storage.retrieve_token("non_existent") is None

        # Test retrieving an existing token
        storage.store_token("test_key", "test_token")
        assert storage.retrieve_token("test_key") == "test_token"

    def test_delete_token(self) -> None:
        """Test deleting a token."""
        storage = InMemoryTokenStorage()

        # Test deleting a non-existent token (should not raise)
        storage.delete_token("non_existent")

        # Test deleting an existing token
        storage.store_token("test_key", "test_token")
        assert "test_key" in storage._storage
        storage.delete_token("test_key")
        assert "test_key" not in storage._storage

    def test_store_and_retrieve_complex_token_data(self) -> None:
        """Test storing and retrieving complex token data (dict)."""
        storage = InMemoryTokenStorage()
        token_data = {
            "access_token": "abc123",
            "refresh_token": "xyz789",
            "expires_in": 3600,
            "token_type": "bearer",
        }

        storage.store_token("complex", token_data)
        retrieved = storage.retrieve_token("complex")

        assert retrieved == token_data
        assert retrieved["access_token"] == "abc123"
        assert retrieved["refresh_token"] == "xyz789"
