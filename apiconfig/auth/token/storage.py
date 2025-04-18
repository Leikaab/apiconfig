import abc
from typing import Any, Dict, Optional


class TokenStorage(abc.ABC):
    """Abstract base class for token storage mechanisms."""

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
    """Stores tokens in an in-memory dictionary."""

    def __init__(self) -> None:
        self._storage: Dict[str, Any] = {}

    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data in the internal dictionary."""
        self._storage[key] = token_data

    def retrieve_token(self, key: str) -> Optional[Any]:
        """Retrieve token data from the internal dictionary."""
        return self._storage.get(key)

    def delete_token(self, key: str) -> None:
        """Delete token data from the internal dictionary."""
        if key in self._storage:
            del self._storage[key]
