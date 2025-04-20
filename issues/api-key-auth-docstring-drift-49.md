---
title: "Docstring drift between auth/strategies/api_key.py and api_key.pyi"
severity: medium
location: "apiconfig/auth/strategies/api_key.py, apiconfig/auth/strategies/api_key.pyi"
github_issue:
  number: 49
  url: "https://github.com/Leikaab/apiconfig/issues/49"
  state: OPEN
  createdAt: "2025-04-19T23:57:57Z"
  updatedAt: "2025-04-19T23:57:57Z"
  author:
    login: "Leikaab"
    id: "MDQ6VXNlcjQ5NzkxNzAx"
  id: "I_kwDOObjluc6zNsgZ"
  assignees: []
  labels: []
---

## Summary
The `apiconfig/auth/strategies/api_key.pyi` stub provides a detailed class-level docstring and method docstrings for `ApiKeyAuth`, including argument descriptions and raised exceptions. The implementation file `api_key.py` has no class or method docstrings. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/auth/strategies/api_key.py
class ApiKeyAuth(AuthStrategy):
    # No class or method docstrings

# apiconfig/auth/strategies/api_key.pyi
class ApiKeyAuth(AuthStrategy):
    """
    Implements API Key authentication.

    The API key can be sent either in a request header or as a query parameter.

    Args:
        api_key: The API key string.
        header_name: The name of the HTTP header to use for the API key.
        param_name: The name of the query parameter to use for the API key.

    Raises:
        AuthStrategyError: If neither or both `header_name` and `param_name` are provided.
    """

    def prepare_request_headers(self) -> Dict[str, str]:
        """
        Prepares headers for API key authentication if configured for headers.

        Returns:
            A dictionary containing the API key header, or an empty dictionary.
        """
        ...

    def prepare_request_params(self) -> Dict[str, str]:
        """
        Prepares query parameters for API key authentication if configured for parameters.

        Returns:
            A dictionary containing the API key parameter, or an empty dictionary.
        """
        ...
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the `ApiKeyAuth` class.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add class and method docstrings to `api_key.py` to match the detail and structure of the `.pyi` stub.
- Ensure future changes to class and method documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.