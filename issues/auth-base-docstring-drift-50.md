---
issue_number: 50
title: "Docstring drift between auth/base.py and auth/base.pyi"
state: OPEN
url: https://github.com/Leikaab/apiconfig/issues/50
author:
  login: Leikaab
  id: MDQ6VXNlcjQ5NzkxNzAx
created_at: 2025-04-19T23:59:03Z
updated_at: 2025-04-19T23:59:03Z
assignees: []
labels: []
---

## Summary
The `apiconfig/auth/base.pyi` stub provides detailed docstrings for the `AuthStrategy` class and its methods, including descriptions, expected behavior, and raised exceptions. The implementation file `base.py` only has brief docstrings, lacking this detail. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/auth/base.py
class AuthStrategy(ABC):
    """Abstract base class for defining authentication strategies."""

    @abstractmethod
    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepare authentication headers for an HTTP request.
        Returns:
            A dictionary containing header names and values.
        """
        pass

# apiconfig/auth/base.pyi
class AuthStrategy(ABC):
    """
    Abstract base class for defining authentication strategies.

    This class provides a common interface for different authentication
    methods (e.g., Basic Auth, Bearer Token, API Key). Subclasses must
    implement the abstract methods to provide the specific logic for
    preparing request headers and/or parameters.
    """

    @abstractmethod
    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepare authentication headers for an HTTP request.

        This method should generate the necessary HTTP headers required
        by the specific authentication strategy.

        Raises:
            AuthStrategyError: If headers cannot be prepared (e.g., missing credentials).

        Returns:
            A dictionary containing header names and values. An empty
            dictionary should be returned if the strategy does not require headers.
        """
        ...
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the base authentication interface.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Update the docstrings in `auth/base.py` to match the detail and structure of the `.pyi` stub.
- Ensure future changes to class and method documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.