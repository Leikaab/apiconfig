---
title: "Docstring drift between auth/strategies/bearer.py and bearer.pyi"
severity: medium
location: "apiconfig/auth/strategies/bearer.py, apiconfig/auth/strategies/bearer.pyi"
---

## Summary
The `apiconfig/auth/strategies/bearer.pyi` stub provides a class-level docstring and detailed method docstrings for `BearerAuth`, including argument and return value descriptions. The implementation file `bearer.py` has no class or method docstrings. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/auth/strategies/bearer.py
class BearerAuth(AuthStrategy):
    # No class or method docstrings

# apiconfig/auth/strategies/bearer.pyi
class BearerAuth(AuthStrategy):
    """
    Implements Bearer Token authentication.

    This strategy adds an 'Authorization: Bearer <token>' header to requests.
    """

    def __init__(self, token: str) -> None:
        """
        Initializes the BearerAuth strategy.

        Args:
            token: The bearer token to use for authentication.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepares the 'Authorization' header with the bearer token.

        Returns:
            A dictionary containing the 'Authorization' header.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Bearer authentication does not typically modify query parameters.

        Returns:
            An empty dictionary.
        """
        ...
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the `BearerAuth` class.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add class and method docstrings to `bearer.py` to match the detail and structure of the `.pyi` stub.
- Ensure future changes to class and method documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.