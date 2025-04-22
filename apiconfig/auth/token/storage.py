"""Abstract base classes and in-memory implementation for token storage."""

import abc
from typing import Any, Dict, Optional


class TokenStorage(abc.ABC):
    """
    Abstract base class for token storage mechanisms.

    This class defines the interface for storing, retrieving, and deleting
    authentication tokens.
    """

    @abc.abstractmethod
    def store_token(self, key: str, token_data: Any) -> None:
        """
        Store token data associated with a key.

        Parameters
        ----------
        key : str
            The unique identifier for the token.
        token_data : Any
            The token data to store (e.g., a string, dictionary).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_token(self, key: str) -> Optional[Any]:
        """
        Retrieve token data associated with a key.

        Parameters
        ----------
        key : str
            The unique identifier for the token.

        Returns
        -------
        Optional[Any]
            The stored token data, or None if the key is not found.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_token(self, key: str) -> None:
        """
        Delete token data associated with a key.

        Parameters
        ----------
        key : str
            The unique identifier for the token to delete.
        """
        raise NotImplementedError


class InMemoryTokenStorage(TokenStorage):
    """
    Stores tokens in an in-memory dictionary.

    This storage is ephemeral and will lose all tokens when the application
    instance terminates. Suitable for testing or short-lived processes.
    """

    _storage: Dict[str, Any]

    def __init__(self) -> None:
        """Initialize the in-memory storage dictionary."""
        self._storage: Dict[str, Any] = {}

    def store_token(self, key: str, token_data: Any) -> None:
        """
        Store token data in the internal dictionary.

        Parameters
        ----------
        key : str
            The unique identifier for the token.
        token_data : Any
            The token data to store.
        """
        self._storage[key] = token_data

    def retrieve_token(self, key: str) -> Optional[Any]:
        """
        Retrieve token data from the internal dictionary.

        Parameters
        ----------
        key : str
            The unique identifier for the token.

        Returns
        -------
        Optional[Any]
            The stored token data, or None if the key is not found.
        """
        return self._storage.get(key)

    def delete_token(self, key: str) -> None:
        """
        Delete token data from the internal dictionary.

        If the key does not exist, this method does nothing.

        Parameters
        ----------
        key : str
            The unique identifier for the token to delete.
        """
        if key in self._storage:
            del self._storage[key]
