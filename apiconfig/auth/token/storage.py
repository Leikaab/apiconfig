import abc
from typing import Any, Dict, Optional


class TokenStorage(abc.ABC):

    @abc.abstractmethod
    def store_token(self, key: str, token_data: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_token(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_token(self, key: str) -> None:
        raise NotImplementedError


class InMemoryTokenStorage(TokenStorage):

    def __init__(self) -> None:
        self._storage: Dict[str, Any] = {}

    def store_token(self, key: str, token_data: Any) -> None:
        self._storage[key] = token_data

    def retrieve_token(self, key: str) -> Optional[Any]:
        return self._storage.get(key)

    def delete_token(self, key: str) -> None:
        if key in self._storage:
            del self._storage[key]
