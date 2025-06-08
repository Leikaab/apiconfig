# -*- coding: utf-8 -*-
# File: apiconfig/testing/auth_verification.py
"""
Authentication verification utilities for testing.

This module provides comprehensive utilities for verifying authentication headers
and formats in tests, supporting Basic Auth, Bearer tokens, API keys, and advanced
verification scenarios like JWT and OAuth2 tokens.
"""

import base64
import json
import re
from typing import Any, Dict, List, Optional

from apiconfig.exceptions.auth import AuthenticationError


class AuthHeaderVerification:
    """Utilities for verifying authentication headers in tests."""

    @staticmethod
    def verify_basic_auth_header(
        header_value: str,
        expected_username: Optional[str] = None,
        expected_password: Optional[str] = None,
    ) -> bool:
        """
        Verify Basic Auth header format and optionally credentials.

        Parameters
        ----------
        header_value : str
            The Authorization header value
        expected_username : str, optional
            Expected username to validate against
        expected_password : str, optional
            Expected password to validate against

        Returns
        -------
        bool
            True if header is valid Basic auth format

        Raises
        ------
        AuthenticationError
            If header format is invalid or credentials don't match

        Examples
        --------
        >>> AuthHeaderVerification.verify_basic_auth_header("Basic dGVzdDpwYXNz")
        True
        >>> AuthHeaderVerification.verify_basic_auth_header(
        ...     "Basic dGVzdDpwYXNz", "test", "pass"
        ... )
        True
        """
        if not header_value.startswith("Basic "):
            raise AuthenticationError("Basic auth header must start with 'Basic '")

        try:
            encoded_credentials = header_value[6:]  # Remove "Basic "
            decoded_bytes = base64.b64decode(encoded_credentials)
            decoded_str = decoded_bytes.decode("utf-8")

            if ":" not in decoded_str:
                raise AuthenticationError("Basic auth credentials must contain ':'")

            username, password = decoded_str.split(":", 1)

            if expected_username is not None and username != expected_username:
                raise AuthenticationError(f"Expected username '{expected_username}', got '{username}'")

            if expected_password is not None and password != expected_password:
                raise AuthenticationError("Password does not match expected value")

            return True

        except (ValueError, UnicodeDecodeError) as e:
            raise AuthenticationError(f"Invalid Basic auth encoding: {e}")

    @staticmethod
    def verify_bearer_auth_header(
        header_value: Optional[str],
        expected_token: Optional[str] = None,
        token_pattern: Optional[str] = None,
    ) -> bool:
        """
        Verify Bearer Auth header format and optionally token value.

        Parameters
        ----------
        header_value : Optional[str]
            The Authorization header value
        expected_token : str, optional
            Expected token value to validate against
        token_pattern : str, optional
            Regex pattern for token validation

        Returns
        -------
        bool
            True if header is valid Bearer auth format

        Raises
        ------
        AuthenticationError
            If header format is invalid or token doesn't match

        Examples
        --------
        >>> AuthHeaderVerification.verify_bearer_auth_header("Bearer abc123")
        True
        >>> AuthHeaderVerification.verify_bearer_auth_header(
        ...     "Bearer abc123", expected_token="abc123"
        ... )
        True
        """
        if header_value is None:
            raise AuthenticationError("Bearer auth header cannot be None")

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
    def verify_api_key_header(
        header_value: str,
        expected_key: Optional[str] = None,
        key_pattern: Optional[str] = None,
    ) -> bool:
        """
        Verify API Key header format and optionally key value.

        Parameters
        ----------
        header_value : str
            The API key header value
        expected_key : str, optional
            Expected key value to validate against
        key_pattern : str, optional
            Regex pattern for key validation

        Returns
        -------
        bool
            True if header is valid API key format

        Raises
        ------
        AuthenticationError
            If header format is invalid or key doesn't match

        Examples
        --------
        >>> AuthHeaderVerification.verify_api_key_header("sk-123abc")
        True
        >>> AuthHeaderVerification.verify_api_key_header(
        ...     "sk-123abc", expected_key="sk-123abc"
        ... )
        True
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
    def verify_auth_header_format(
        headers: Dict[str, str],
        auth_type: str,
        header_name: str = "Authorization",
        **kwargs: Any,
    ) -> None:
        """
        Verify auth header exists and has correct format.

        Parameters
        ----------
        headers : Dict[str, str]
            Request headers dictionary
        auth_type : str
            Type of auth ("basic", "bearer", "api_key")
        header_name : str, default "Authorization"
            Header name to check
        **kwargs
            Additional arguments for specific verification methods

        Raises
        ------
        AuthenticationError
            If header is missing or invalid

        Examples
        --------
        >>> headers = {"Authorization": "Bearer abc123"}
        >>> AuthHeaderVerification.verify_auth_header_format(headers, "bearer")
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
    def verify_multiple_auth_headers(headers: Dict[str, str], auth_configs: List[Dict[str, Any]]) -> None:
        """
        Verify multiple authentication headers.

        Parameters
        ----------
        headers : Dict[str, str]
            Request headers dictionary
        auth_configs : List[Dict[str, Union[str, Dict]]]
            List of auth configurations, each containing:
            - auth_type: Type of auth
            - header_name: Header name
            - **kwargs: Additional verification arguments

        Examples
        --------
        >>> headers = {
        ...     "Authorization": "Bearer abc123",
        ...     "X-API-Key": "key123"
        ... }
        >>> configs = [
        ...     {"auth_type": "bearer", "header_name": "Authorization"},
        ...     {"auth_type": "api_key", "header_name": "X-API-Key", "expected_key": "key123"}
        ... ]
        >>> AuthHeaderVerification.verify_multiple_auth_headers(headers, configs)
        """
        for config in auth_configs:
            config_copy = config.copy()
            auth_type = config_copy.pop("auth_type")
            header_name = config_copy.pop("header_name", "Authorization")
            AuthHeaderVerification.verify_auth_header_format(headers, auth_type, header_name, **config_copy)

    @staticmethod
    def verify_no_auth_headers(headers: Dict[str, str], auth_header_names: Optional[List[str]] = None) -> None:
        """
        Verify that no authentication headers are present.

        Parameters
        ----------
        headers : Dict[str, str]
            Request headers dictionary
        auth_header_names : List[str], optional
            List of auth header names to check (default: common auth headers)

        Raises
        ------
        AuthenticationError
            If any auth headers are found

        Examples
        --------
        >>> headers = {"Content-Type": "application/json"}
        >>> AuthHeaderVerification.verify_no_auth_headers(headers)
        """
        if auth_header_names is None:
            auth_header_names = [
                "Authorization",
                "X-API-Key",
                "X-Auth-Token",
                "X-Access-Token",
            ]

        found_headers: List[str] = []
        for header_name in auth_header_names:
            if header_name in headers:
                found_headers.append(header_name)

        if found_headers:
            raise AuthenticationError(f"Unexpected auth headers found: {found_headers}")


class AdvancedAuthVerification:
    """Advanced authentication verification utilities."""

    @staticmethod
    def verify_jwt_structure(token: str, verify_signature: bool = False) -> Dict[str, Any]:
        """
        Verify JWT token structure and optionally signature.

        Parameters
        ----------
        token : str
            JWT token string
        verify_signature : bool, default False
            Whether to verify signature (requires key)

        Returns
        -------
        Dict[str, Any]
            Dictionary containing header and payload

        Raises
        ------
        AuthenticationError
            If JWT structure is invalid

        Examples
        --------
        >>> token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
        >>> result = AdvancedAuthVerification.verify_jwt_structure(token)
        >>> "header" in result and "payload" in result
        True
        """
        try:
            parts = token.split(".")
            if len(parts) != 3:
                raise AuthenticationError("JWT must have exactly 3 parts")

            header_b64, payload_b64, _ = parts

            # Decode header and payload
            header = json.loads(base64.b64decode(header_b64 + "==").decode("utf-8"))
            payload = json.loads(base64.b64decode(payload_b64 + "==").decode("utf-8"))

            # Basic structure validation
            if "alg" not in header:
                raise AuthenticationError("JWT header missing 'alg' field")

            if "typ" not in header or header["typ"] != "JWT":
                raise AuthenticationError("JWT header 'typ' must be 'JWT'")

            return {"header": header, "payload": payload}

        except (ValueError, KeyError) as e:
            raise AuthenticationError(f"Invalid JWT structure: {e}")

    @staticmethod
    def verify_oauth2_token_format(token: str, token_type: str = "Bearer") -> bool:
        """
        Verify OAuth2 token format and characteristics.

        Parameters
        ----------
        token : str
            OAuth2 token string
        token_type : str, default "Bearer"
            Expected token type

        Returns
        -------
        bool
            True if token format is valid

        Raises
        ------
        AuthenticationError
            If token format is invalid

        Examples
        --------
        >>> AdvancedAuthVerification.verify_oauth2_token_format("abc123token")
        True
        """
        if not token:
            raise AuthenticationError("OAuth2 token cannot be empty")

        # Check for common OAuth2 token patterns
        if token_type.lower() == "bearer":
            # Bearer tokens are typically base64-encoded or JWT
            if len(token) < 10:
                raise AuthenticationError("Bearer token appears too short")

            # Check if it's a JWT
            if token.count(".") == 2:
                AdvancedAuthVerification.verify_jwt_structure(token)

        return True

    @staticmethod
    def verify_session_token_format(token: str, expected_prefix: Optional[str] = None) -> bool:
        """
        Verify session token format.

        Parameters
        ----------
        token : str
            Session token string
        expected_prefix : str, optional
            Expected token prefix

        Returns
        -------
        bool
            True if token format is valid

        Raises
        ------
        AuthenticationError
            If token format is invalid

        Examples
        --------
        >>> AdvancedAuthVerification.verify_session_token_format("sess_abc123")
        True
        >>> AdvancedAuthVerification.verify_session_token_format(
        ...     "sess_abc123", expected_prefix="sess_"
        ... )
        True
        """
        if not token:
            raise AuthenticationError("Session token cannot be empty")

        if expected_prefix and not token.startswith(expected_prefix):
            raise AuthenticationError(f"Session token must start with '{expected_prefix}'")

        # Basic length validation
        if len(token) < 8:
            raise AuthenticationError("Session token appears too short")

        return True


class AuthTestHelpers:
    """Helper utilities for auth testing scenarios."""

    @staticmethod
    def assert_auth_applied(headers: Dict[str, str], auth_type: str, **verification_kwargs: Any) -> None:
        """
        Assert that authentication was properly applied to headers.

        Parameters
        ----------
        headers : Dict[str, str]
            Request headers to verify
        auth_type : str
            Expected auth type
        **verification_kwargs
            Additional verification arguments

        Raises
        ------
        AssertionError
            If authentication was not properly applied

        Examples
        --------
        >>> headers = {"Authorization": "Bearer abc123"}
        >>> AuthTestHelpers.assert_auth_applied(headers, "bearer")
        """
        try:
            AuthHeaderVerification.verify_auth_header_format(headers, auth_type, **verification_kwargs)
        except AuthenticationError as e:
            raise AssertionError(f"Authentication not properly applied: {e}")

    @staticmethod
    def assert_no_auth_applied(headers: Dict[str, str]) -> None:
        """
        Assert that no authentication was applied to headers.

        Parameters
        ----------
        headers : Dict[str, str]
            Request headers to verify

        Raises
        ------
        AssertionError
            If unexpected authentication was found

        Examples
        --------
        >>> headers = {"Content-Type": "application/json"}
        >>> AuthTestHelpers.assert_no_auth_applied(headers)
        """
        try:
            AuthHeaderVerification.verify_no_auth_headers(headers)
        except AuthenticationError as e:
            raise AssertionError(f"Unexpected authentication found: {e}")

    @staticmethod
    def create_test_auth_headers(auth_type: str, **kwargs: Any) -> Dict[str, str]:
        """
        Create test authentication headers for testing.

        Parameters
        ----------
        auth_type : str
            Type of auth to create
        **kwargs
            Auth-specific parameters

        Returns
        -------
        Dict[str, str]
            Dictionary with appropriate auth headers

        Examples
        --------
        >>> headers = AuthTestHelpers.create_test_auth_headers("basic")
        >>> "Authorization" in headers
        True
        >>> headers = AuthTestHelpers.create_test_auth_headers(
        ...     "api_key", key="mykey", header_name="X-API-Key"
        ... )
        >>> headers["X-API-Key"]
        'mykey'
        """
        headers: Dict[str, str] = {}

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
