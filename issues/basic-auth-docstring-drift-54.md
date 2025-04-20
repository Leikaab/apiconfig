---
title: "Docstring drift between auth/strategies/basic.py and basic.pyi"
issue_number: 54
issue_id: I_kwDOObjluc6zNtAp
github_url: "https://github.com/Leikaab/apiconfig/issues/54"
state: OPEN
created_at: "2025-04-20T00:04:30Z"
updated_at: "2025-04-20T00:04:30Z"
author: "Leikaab"
author_id: "MDQ6VXNlcjQ5NzkxNzAx"
assignees: []
labels: []
severity: medium
location: "apiconfig/auth/strategies/basic.py, apiconfig/auth/strategies/basic.pyi"
---

## Summary
The `apiconfig/auth/strategies/basic.pyi` stub provides a class-level docstring and detailed method docstrings for `BasicAuth`, including argument and return value descriptions. The implementation file `basic.py` has no class or method docstrings. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/auth/strategies/basic.py
class BasicAuth(AuthStrategy):
    # No class or method docstrings

# apiconfig/auth/strategies/basic.pyi
class BasicAuth(AuthStrategy):
    """
    Implements HTTP Basic Authentication.

    This strategy adds the 'Authorization' header with Basic credentials
    (base64-encoded username:password) to the request.
    """

    def __init__(self, username: str, password: str) -> None:
        """
        Initializes the BasicAuth strategy.

        Args:
            username: The username for authentication.
            password: The password for authentication.
        """
        ...

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Generates the 'Authorization' header for Basic Authentication.

        Returns:
            A dictionary containing the 'Authorization' header.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Returns an empty dictionary as Basic Auth uses headers, not params.

        Returns:
            An empty dictionary.
        """
        ...
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the `BasicAuth` class.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add class and method docstrings to `basic.py` to match the detail and structure of the `.pyi` stub.
- Ensure future changes to class and method documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.