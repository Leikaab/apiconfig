import abc
from typing import Any, Dict, Optional


class TokenStorage(abc.ABC):
    """Base class for token storage mechanisms."""

    @abc.abstractmethod
    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data associated with a key."""
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_token(self, key: str) -> Optional[Any]:
        """Retrieve token data associated with a key."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete_token(self, key: str) -> None:
        """Delete token data associated with a key."""
        raise NotImplementedError


class InMemoryTokenStorage(TokenStorage):
    """In-memory token storage implementation."""

    def __init__(self) -> None:
        self._storage: Dict[str, Any] = {}

    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data in memory."""
        self._storage[key] = token_data

    def retrieve_token(self, key: str) -> Optional[Any]:
        """Retrieve token data from memory."""
        return self._storage.get(key)

    def delete_token(self, key: str) -> None:
        """Delete token data from memory."""
        if key in self._storage:
            del self._storage[key]
