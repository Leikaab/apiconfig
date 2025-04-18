import abc
from typing import Any, Dict, Optional


class TokenStorage(abc.ABC):
    """Abstract base class for token storage mechanisms."""

    @abc.abstractmethod
    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data associated with a key.

        Args:
            key: The unique identifier for the token.
            token_data: The token data to store (e.g., a string, dictionary).
        """
        ...

    @abc.abstractmethod
    def retrieve_token(self, key: str) -> Optional[Any]:
        """Retrieve token data associated with a key.

        Args:
            key: The unique identifier for the token.

        Returns:
            The stored token data, or None if the key is not found.
        """
        ...

    @abc.abstractmethod
    def delete_token(self, key: str) -> None:
        """Delete token data associated with a key.

        Args:
            key: The unique identifier for the token to delete.
        """
        ...


class InMemoryTokenStorage(TokenStorage):
    """Stores tokens in an in-memory dictionary.

    This storage is ephemeral and will lose all tokens when the application
    instance terminates. Suitable for testing or short-lived processes.
    """

    _storage: Dict[str, Any]

    def __init__(self) -> None: ...

    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data in the internal dictionary.

        Args:
            key: The unique identifier for the token.
            token_data: The token data to store.
        """
        ...

    def retrieve_token(self, key: str) -> Optional[Any]:
        """Retrieve token data from the internal dictionary.

        Args:
            key: The unique identifier for the token.

        Returns:
            The stored token data, or None if the key is not found.
        """
        ...

    def delete_token(self, key: str) -> None:
        """Delete token data from the internal dictionary.

        If the key does not exist, this method does nothing.

        Args:
            key: The unique identifier for the token to delete.
        """
        ...
