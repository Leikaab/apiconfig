---
issue_number: 75
title: "Docstring drift between auth/token/storage.py and storage.pyi"
url: "https://github.com/Leikaab/apiconfig/issues/75"
state: OPEN
createdAt: "2025-04-20T00:42:58Z"
updatedAt: "2025-04-20T00:42:58Z"
author:
  login: "Leikaab"
  id: "MDQ6VXNlcjQ5NzkxNzAx"
assignees:
  - login: "Leikaab"
    id: "MDQ6VXNlcjQ5NzkxNzAx"
severity: medium
location: "apiconfig/auth/token/storage.py, apiconfig/auth/token/storage.pyi"
---

## Summary
The `apiconfig/auth/token/storage.pyi` stub provides detailed docstrings for all methods and classes, including argument and return value descriptions, and notes about behavior. The implementation file `storage.py` has only brief docstrings for classes and methods, lacking argument and return value details. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/auth/token/storage.py
class TokenStorage(abc.ABC):
    """Abstract base class for token storage mechanisms."""

    @abc.abstractmethod
    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data associated with a key."""
        raise NotImplementedError

    # ... (other methods similar)

class InMemoryTokenStorage(TokenStorage):
    """Stores tokens in an in-memory dictionary."""

    def store_token(self, key: str, token_data: Any) -> None:
        """Store token data in the internal dictionary."""
        self._storage[key] = token_data

    # ... (other methods similar)

# apiconfig/auth/token/storage.pyi
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

    # ... (other methods and classes have similar detailed docstrings)
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the token storage classes.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add detailed docstrings to `storage.py` methods and classes to match the `.pyi` stub, including argument and return value descriptions.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.