# apiconfig.exceptions

`apiconfig.exceptions` contains the exception hierarchy used throughout the
**apiconfig** project. All exceptions derive from `APIConfigError`, and the
modules are grouped by domain: authentication, configuration and HTTP utilities.

Importing from `apiconfig.exceptions` gives quick access to the most commonly
used classes without reaching into each submodule.

## Module Description
This package centralises all error classes used by **apiconfig**. By defining
a consistent hierarchy rooted at `APIConfigError`, it allows callers to handle
failures uniformly across authentication, configuration and HTTP utilities.

The hierarchy solves the problem of disparate error handling. Each subpackage
raises these exceptions, enabling a consumer to catch a specific subclass when
needed or handle general issues by catching `APIConfigError`. This approach is
used throughout the project, from the authentication layer to configuration
parsers and HTTP helpers.

Base classes such as `AuthenticationError` and `ConfigurationError` derive from
`APIConfigError`, while specialised classes inherit from these bases. Factory
helpers map HTTP status codes to the correct subclass, keeping error handling
both explicit and extensible.

## Navigation
- [Back to parent module](../README.md)
- **Modules**
  - `base.py` – Core base classes and mixins.
  - `auth.py` – Authentication-related errors.
  - `config.py` – Configuration loading and validation errors.
  - `http.py` – HTTP and API client errors.

## Contents
- `base.py` – core base classes and mixins.
- `auth.py` – authentication related errors, including token refresh failures.
- `config.py` – configuration loading and validation errors.
- `http.py` – HTTP and API client errors, JSON encode/decode helpers.
- `__init__.py` – re-exports all exceptions for convenience.

## Example usage
```python
from apiconfig.exceptions import (
    InvalidCredentialsError,
    create_api_client_error,
)

# Raised when login credentials fail validation
raise InvalidCredentialsError("Bad username/password")

# Convert an HTTP status code to the correct error subclass
err = create_api_client_error(404)
print(type(err))  # <class 'apiconfig.exceptions.http.ApiClientNotFoundError'>
```

## Key classes
| Class | Description |
| ----- | ----------- |
| `APIConfigError` | Base class for all apiconfig errors. |
| `AuthenticationError` | Base for authentication failures and token refresh issues. |
| `ConfigurationError` | Base for configuration loading errors. |
| `HTTPUtilsError` | Base for errors raised by HTTP helpers. |
| `ApiClientError` | Base for HTTP API client errors with request/response context. |

### Design
The exceptions follow a simple inheritance tree allowing you to catch broad
categories or specific errors as needed.

```mermaid
graph TD
    APIConfigError --> AuthenticationError
    APIConfigError --> ConfigurationError
    APIConfigError --> HTTPUtilsError
    AuthenticationError --> InvalidCredentialsError
    AuthenticationError --> ExpiredTokenError
    AuthenticationError --> MissingCredentialsError
    AuthenticationError --> TokenRefreshError
    TokenRefreshError --> TokenRefreshJsonError
    TokenRefreshError --> TokenRefreshTimeoutError
    TokenRefreshError --> TokenRefreshNetworkError
    HTTPUtilsError --> ApiClientError
    ApiClientError --> ApiClientBadRequestError
    ApiClientError --> ApiClientUnauthorizedError
    ApiClientError --> ApiClientForbiddenError
    ApiClientError --> ApiClientNotFoundError
    ApiClientError --> ApiClientConflictError
    ApiClientError --> ApiClientUnprocessableEntityError
    ApiClientError --> ApiClientRateLimitError
    ApiClientError --> ApiClientInternalServerError
```

## Testing
Install dependencies and run the unit tests for this package:
```bash
poetry install --with dev
poetry run pytest tests/unit/exceptions -q
```

## Dependencies

### Standard Library
- `typing` – used for type annotations in the exceptions.
- `http` – provides HTTP status codes for certain errors.

### Internal Modules
- `apiconfig.utils.http` – helpers used when raising client errors.

## See Also
- [auth](../auth/README.md) – strategies that raise authentication errors
- [config](../config/README.md) – configuration providers that emit errors

## Status
Stable – exceptions are widely used across the library and covered by unit
tests.

**Stability:** Stable
**API Version:** 0.3.1
**Deprecations:** None

### Maintenance Notes
- Exception hierarchy is stable; new exceptions added as needed.

### Changelog
- Major changes are noted in the project changelog.

### Future Considerations
- Possible expansion for async error handling.

