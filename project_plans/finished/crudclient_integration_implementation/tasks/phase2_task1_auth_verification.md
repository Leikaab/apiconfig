# Phase 2, Task 1: Auth Verification Utilities

## Overview
Create [`apiconfig/testing/auth_verification.py`](/workspace/apiconfig/testing/auth_verification.py) with comprehensive utilities for verifying authentication headers and formats, inspired by crudclient's testing utilities.

## Objective
Provide robust testing utilities that both `apiconfig` and `crudclient` can use to verify authentication headers, validate auth formats, and ensure proper authentication implementation in tests.

## Requirements

### 1. AuthHeaderVerification Class
Create a comprehensive class for auth header verification:

```python
# apiconfig/testing/auth_verification.py
import re
import base64
from typing import Dict, Optional, Union, List
from apiconfig.exceptions.auth import AuthenticationError

class AuthHeaderVerification:
    """Utilities for verifying authentication headers in tests."""

    @staticmethod
    def verify_basic_auth_header(header_value: str, expected_username: Optional[str] = None, expected_password: Optional[str] = None) -> bool:
        """
        Verify Basic Auth header format and optionally credentials.

        Args:
            header_value: The Authorization header value
            expected_username: Optional expected username
            expected_password: Optional expected password

        Returns:
            bool: True if header is valid Basic auth format

        Raises:
            AuthenticationError: If header format is invalid
        """
        if not header_value.startswith("Basic "):
            raise AuthenticationError("Basic auth header must start with 'Basic '")

        try:
            encoded_credentials = header_value[6:]  # Remove "Basic "
            decoded_bytes = base64.b64decode(encoded_credentials)
            decoded_str = decoded_bytes.decode('utf-8')

            if ':' not in decoded_str:
                raise AuthenticationError("Basic auth credentials must contain ':'")

            username, password = decoded_str.split(':', 1)

            if expected_username is not None and username != expected_username:
                raise AuthenticationError(f"Expected username '{expected_username}', got '{username}'")

            if expected_password is not None and password != expected_password:
                raise AuthenticationError("Password does not match expected value")

            return True

        except (ValueError, UnicodeDecodeError) as e:
            raise AuthenticationError(f"Invalid Basic auth encoding: {e}")

    @staticmethod
    def verify_bearer_auth_header(header_value: str, expected_token: Optional[str] = None, token_pattern: Optional[str] = None) -> bool:
        """
        Verify Bearer Auth header format and optionally token value.

        Args:
            header_value: The Authorization header value
            expected_token: Optional expected token value
            token_pattern: Optional regex pattern for token validation

        Returns:
            bool: True if header is valid Bearer auth format

        Raises:
            AuthenticationError: If header format is invalid
        """
        if not header_value.startswith("Bearer "):
            raise AuthenticationError("Bearer auth header must start with 'Bearer '")

        token = header_value[7:]  # Remove "Bearer "

        if not token:
            raise AuthenticationError("Bearer token cannot be empty")

        if expected_token is not None and token != expected_token:
            raise AuthenticationError(f"Expected token '{expected_token}', got '{token}'")

        if token_pattern is not None:
            if not re.match(token_pattern, token):
                raise AuthenticationError(f"Token does not match pattern '{token_pattern}'")

        return True

    @staticmethod
    def verify_api_key_header(header_value: str, expected_key: Optional[str] = None, key_pattern: Optional[str] = None) -> bool:
        """
        Verify API Key header format and optionally key value.

        Args:
            header_value: The API key header value
            expected_key: Optional expected key value
            key_pattern: Optional regex pattern for key validation

        Returns:
            bool: True if header is valid API key format

        Raises:
            AuthenticationError: If header format is invalid
        """
        if not header_value:
            raise AuthenticationError("API key header cannot be empty")

        if expected_key is not None and header_value != expected_key:
            raise AuthenticationError(f"Expected key '{expected_key}', got '{header_value}'")

        if key_pattern is not None:
            if not re.match(key_pattern, header_value):
                raise AuthenticationError(f"API key does not match pattern '{key_pattern}'")

        return True

    @staticmethod
    def verify_auth_header_format(headers: Dict[str, str], auth_type: str, header_name: str = "Authorization", **kwargs) -> None:
        """
        Verify auth header exists and has correct format.

        Args:
            headers: Request headers dictionary
            auth_type: Type of auth ("basic", "bearer", "api_key")
            header_name: Header name to check (default: "Authorization")
            **kwargs: Additional arguments for specific verification methods

        Raises:
            AuthenticationError: If header is missing or invalid
        """
        if header_name not in headers:
            raise AuthenticationError(f"Missing {header_name} header")

        header_value = headers[header_name]

        if auth_type.lower() == "basic":
            AuthHeaderVerification.verify_basic_auth_header(header_value, **kwargs)
        elif auth_type.lower() == "bearer":
            AuthHeaderVerification.verify_bearer_auth_header(header_value, **kwargs)
        elif auth_type.lower() == "api_key":
            AuthHeaderVerification.verify_api_key_header(header_value, **kwargs)
        else:
            raise AuthenticationError(f"Unsupported auth type: {auth_type}")

    @staticmethod
    def verify_multiple_auth_headers(headers: Dict[str, str], auth_configs: List[Dict[str, Union[str, Dict]]]) -> None:
        """
        Verify multiple authentication headers.

        Args:
            headers: Request headers dictionary
            auth_configs: List of auth configurations, each containing:
                - auth_type: Type of auth
                - header_name: Header name
                - **kwargs: Additional verification arguments

        Example:
            verify_multiple_auth_headers(headers, [
                {"auth_type": "bearer", "header_name": "Authorization"},
                {"auth_type": "api_key", "header_name": "X-API-Key", "expected_key": "test123"}
            ])
        """
        for config in auth_configs:
            auth_type = config.pop("auth_type")
            header_name = config.pop("header_name", "Authorization")
            AuthHeaderVerification.verify_auth_header_format(
                headers, auth_type, header_name, **config
            )

    @staticmethod
    def verify_no_auth_headers(headers: Dict[str, str], auth_header_names: Optional[List[str]] = None) -> None:
        """
        Verify that no authentication headers are present.

        Args:
            headers: Request headers dictionary
            auth_header_names: Optional list of auth header names to check
                              (default: common auth headers)

        Raises:
            AuthenticationError: If any auth headers are found
        """
        if auth_header_names is None:
            auth_header_names = ["Authorization", "X-API-Key", "X-Auth-Token", "X-Access-Token"]

        found_headers = []
        for header_name in auth_header_names:
            if header_name in headers:
                found_headers.append(header_name)

        if found_headers:
            raise AuthenticationError(f"Unexpected auth headers found: {found_headers}")
```

### 2. Advanced Verification Methods
Add specialized verification methods for complex scenarios:

```python
class AdvancedAuthVerification:
    """Advanced authentication verification utilities."""

    @staticmethod
    def verify_jwt_structure(token: str, verify_signature: bool = False) -> Dict[str, Any]:
        """
        Verify JWT token structure and optionally signature.

        Args:
            token: JWT token string
            verify_signature: Whether to verify signature (requires key)

        Returns:
            Dict containing header and payload

        Raises:
            AuthenticationError: If JWT structure is invalid
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                raise AuthenticationError("JWT must have exactly 3 parts")

            header_b64, payload_b64, signature_b64 = parts

            # Decode header and payload
            header = json.loads(base64.b64decode(header_b64 + '==').decode('utf-8'))
            payload = json.loads(base64.b64decode(payload_b64 + '==').decode('utf-8'))

            # Basic structure validation
            if 'alg' not in header:
                raise AuthenticationError("JWT header missing 'alg' field")

            if 'typ' not in header or header['typ'] != 'JWT':
                raise AuthenticationError("JWT header 'typ' must be 'JWT'")

            return {"header": header, "payload": payload}

        except (ValueError, KeyError) as e:
            raise AuthenticationError(f"Invalid JWT structure: {e}")

    @staticmethod
    def verify_oauth2_token_format(token: str, token_type: str = "Bearer") -> bool:
        """
        Verify OAuth2 token format and characteristics.

        Args:
            token: OAuth2 token string
            token_type: Expected token type

        Returns:
            bool: True if token format is valid
        """
        if not token:
            raise AuthenticationError("OAuth2 token cannot be empty")

        # Check for common OAuth2 token patterns
        if token_type.lower() == "bearer":
            # Bearer tokens are typically base64-encoded or JWT
            if len(token) < 10:
                raise AuthenticationError("Bearer token appears too short")

            # Check if it's a JWT
            if token.count('.') == 2:
                AdvancedAuthVerification.verify_jwt_structure(token)

        return True

    @staticmethod
    def verify_session_token_format(token: str, expected_prefix: Optional[str] = None) -> bool:
        """
        Verify session token format.

        Args:
            token: Session token string
            expected_prefix: Optional expected token prefix

        Returns:
            bool: True if token format is valid
        """
        if not token:
            raise AuthenticationError("Session token cannot be empty")

        if expected_prefix and not token.startswith(expected_prefix):
            raise AuthenticationError(f"Session token must start with '{expected_prefix}'")

        # Basic length validation
        if len(token) < 8:
            raise AuthenticationError("Session token appears too short")

        return True
```

### 3. Test Integration Helpers
Add helpers for common test scenarios:

```python
class AuthTestHelpers:
    """Helper utilities for auth testing scenarios."""

    @staticmethod
    def assert_auth_applied(headers: Dict[str, str], auth_type: str, **verification_kwargs) -> None:
        """
        Assert that authentication was properly applied to headers.

        Args:
            headers: Request headers to verify
            auth_type: Expected auth type
            **verification_kwargs: Additional verification arguments
        """
        try:
            AuthHeaderVerification.verify_auth_header_format(
                headers, auth_type, **verification_kwargs
            )
        except AuthenticationError as e:
            raise AssertionError(f"Authentication not properly applied: {e}")

    @staticmethod
    def assert_no_auth_applied(headers: Dict[str, str]) -> None:
        """
        Assert that no authentication was applied to headers.

        Args:
            headers: Request headers to verify
        """
        try:
            AuthHeaderVerification.verify_no_auth_headers(headers)
        except AuthenticationError as e:
            raise AssertionError(f"Unexpected authentication found: {e}")

    @staticmethod
    def create_test_auth_headers(auth_type: str, **kwargs) -> Dict[str, str]:
        """
        Create test authentication headers for testing.

        Args:
            auth_type: Type of auth to create
            **kwargs: Auth-specific parameters

        Returns:
            Dict with appropriate auth headers
        """
        headers = {}

        if auth_type.lower() == "basic":
            username = kwargs.get("username", "testuser")
            password = kwargs.get("password", "testpass")
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"

        elif auth_type.lower() == "bearer":
            token = kwargs.get("token", "test_bearer_token")
            headers["Authorization"] = f"Bearer {token}"

        elif auth_type.lower() == "api_key":
            key = kwargs.get("key", "test_api_key")
            header_name = kwargs.get("header_name", "X-API-Key")
            headers[header_name] = key

        return headers
```

## Implementation Steps

1. **Create the auth_verification.py file** in the testing module
2. **Implement AuthHeaderVerification class** with basic verification methods
3. **Add AdvancedAuthVerification class** for complex scenarios
4. **Create AuthTestHelpers class** for test integration
5. **Add comprehensive docstrings** and examples
6. **Create unit tests** for all verification methods
7. **Add integration examples** showing usage patterns
8. **Update testing module exports** to include new utilities

## Files to Create/Modify
- Create: [`apiconfig/testing/auth_verification.py`](/workspace/apiconfig/testing/auth_verification.py)
- Modify: [`apiconfig/testing/__init__.py`](/workspace/apiconfig/testing/__init__.py) (add exports)

## Dependencies
- [Phase 1 completion](phase1_component_validation.md)

## Quality Gates

### Functionality
- [ ] All auth types properly verified (Basic, Bearer, API Key)
- [ ] Advanced verification for JWT and OAuth2 tokens
- [ ] Helper methods for common test scenarios
- [ ] Comprehensive error handling and messages

### Testing
- [ ] Unit tests for all verification methods
- [ ] Tests for error scenarios and edge cases
- [ ] Integration tests with actual auth strategies
- [ ] Performance tests for verification operations

### Documentation
- [ ] Comprehensive docstrings with examples
- [ ] Usage patterns documented
- [ ] Integration examples provided
- [ ] Error handling guidance

## Success Criteria
- [ ] Comprehensive auth header verification utilities available
- [ ] Support for all major auth types and formats
- [ ] Easy integration with existing test suites
- [ ] Clear error messages for debugging
- [ ] Performance suitable for test environments
- [ ] Extensible design for future auth types

## Notes
- Focus on test utility functionality, not production auth
- Provide clear error messages for test debugging
- Support both positive and negative test scenarios
- Consider performance for large test suites
- Design for extensibility with new auth types

## Estimated Effort
4-5 hours

## Next Task
[Phase 2, Task 2: Enhanced Auth Mocks](phase2_task2_enhanced_auth_mocks.md)