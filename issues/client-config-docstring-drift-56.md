---
title: "Docstring drift between config/base.py and base.pyi for ClientConfig"
severity: medium
location: "apiconfig/config/base.py, apiconfig/config/base.pyi"
issue_number: 56
issue_url: https://github.com/Leikaab/apiconfig/issues/56
repo: Leikaab/apiconfig
created_via: GitHub CLI
created_at: 2025-04-20T00:06:23Z
---

## Summary
The `apiconfig/config/base.pyi` stub provides a detailed class-level docstring and method docstrings for `ClientConfig`, including attributes, argument descriptions, return values, and raised exceptions. The implementation file `base.py` has no class-level docstring and only minimal or no docstrings for methods. This leads to incomplete runtime documentation and can confuse users and maintainers.

## Evidence
```python
# apiconfig/config/base.py
class ClientConfig:
    # No class-level docstring
    def __init__(...):
        # No or minimal docstring

    # ... (other methods similar)

# apiconfig/config/base.pyi
class ClientConfig:
    """
    Base configuration class for API clients.

    Stores common configuration settings like hostname, API version, headers,
    timeout, retries, and authentication strategy.

    Attributes:
        hostname: The base hostname of the API (e.g., "api.example.com").
        version: The API version string (e.g., "v1"). Appended to the hostname.
        headers: Default headers to include in every request.
        timeout: Default request timeout in seconds.
        retries: Default number of retries for failed requests.
        auth_strategy: An instance of AuthStrategy for handling authentication.
        log_request_body: Whether to log the request body (potentially sensitive).
        log_response_body: Whether to log the response body (potentially sensitive).
    """

    def __init__(...):
        """
        Initializes the ClientConfig instance.

        Args:
            hostname: The base hostname of the API.
            version: The API version string.
            headers: Default headers for requests.
            timeout: Request timeout in seconds.
            retries: Number of retries for failed requests.
            auth_strategy: Authentication strategy instance.
            log_request_body: Flag to enable request body logging.
            log_response_body: Flag to enable response body logging.

        Raises:
            InvalidConfigError: If timeout or retries are negative.
        """
        ...

    # ... (other methods have similar detailed docstrings)
```

## Impact
- Users relying on runtime docstrings or auto-generated documentation will not see the full contract or expected behavior.
- Increases the risk of misuse or misunderstanding of the `ClientConfig` class.
- Creates a maintenance burden and potential for further drift.

## Suggested Direction
- Add a class-level docstring and detailed method docstrings to `base.py` to match the `.pyi` stub, including attributes, argument descriptions, return values, and raised exceptions.
- Ensure future changes to documentation are made in both files.

## Related
- See other findings on .py ↔ .pyi drift, if any.
- Project documentation and type hinting guidelines.