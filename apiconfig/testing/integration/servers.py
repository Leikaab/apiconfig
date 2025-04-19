# -*- coding: utf-8 -*-
"""
Utilities for managing mock API servers during integration tests.

This module leverages pytest-httpserver to provide a configurable mock server
for testing interactions with external APIs.
"""
from typing import Any, Dict, Optional, Union

from pytest_httpserver import HTTPServer  # type: ignore[import-untyped]
from werkzeug.wrappers import Response


def configure_mock_response(
    httpserver: HTTPServer,
    path: str,
    method: str = "GET",
    response_data: Optional[Union[Dict[str, Any], str]] = None,
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> None:
    """
    Configures a specific response for the mock HTTPServer.

    Args:
        httpserver: The pytest-httpserver fixture instance.
        path: The URL path to match (e.g., "/api/v1/resource").
        method: The HTTP method to match (e.g., "GET", "POST").
        response_data: The JSON data or raw string to return in the response body.
                       If None, an empty body is returned.
        status_code: The HTTP status code to return.
        headers: Optional dictionary of headers to return in the response.
        **kwargs: Additional arguments passed directly to httpserver.expect_request.
                  See pytest-httpserver documentation for options like matching
                  headers, query strings, or request body.
    """
    if headers is None:
        headers = {}

    # Default content type if response_data is a dict (implying JSON)
    if isinstance(response_data, dict) and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    # pytest-httpserver expects response_json for dicts and response_data for strings
    if isinstance(response_data, dict):
        kwargs["response_json"] = response_data
    elif isinstance(response_data, str):
        kwargs["response_data"] = response_data
    # Handle None case implicitly (empty body)

    httpserver.expect_request(
        uri=path, method=method, **kwargs
    ).respond_with_response(
        Response(status=status_code, headers=headers)
    )

# Potential future additions:
# - A context manager or class to manage server setup/teardown if needed.
# - More specific helper functions for common patterns (e.g., auth endpoints).
# - Integration with test data factories.
