# apiconfig/testing/integration/servers.pyi
# -*- coding: utf-8 -*-
"""
Type stubs for mock API server utilities for integration testing.

This module provides utilities for configuring and validating mock HTTP servers
during integration tests. It leverages pytest-httpserver to create configurable
mock servers that can simulate various API behaviors, including authentication
flows, error conditions, and expected responses.

These utilities are particularly useful for:
- Testing client authentication mechanisms against controlled server responses
- Verifying that clients send expected headers, query parameters, and request bodies
- Simulating multi-step API interactions and stateful authentication flows
- Validating error handling in API client code
"""
from typing import Any, Dict, List, Optional, Union

from pytest_httpserver import HTTPServer

def configure_mock_response(
    httpserver: HTTPServer,
    path: str,
    method: str = "GET",
    response_data: Optional[Union[Dict[str, Any], str]] = None,
    status_code: int = 200,
    response_headers: Optional[Dict[str, str]] = None,
    match_headers: Optional[Dict[str, str]] = None,
    match_query_string: Optional[Dict[str, str]] = None,
    match_json: Optional[Any] = None,
    match_data: Optional[str] = None,
    ordered: bool = False,
    **kwargs: Any,
) -> None:
    """
    Configures a specific response expectation for the mock HTTPServer.

    This function allows detailed matching of incoming requests, making it suitable
    for testing various authentication strategies, including custom ones that
    might add specific headers, query parameters, or body content.

    For stateful authentication flows (e.g., challenge-response), call this
    function multiple times in the expected order of requests, setting `ordered=True`.

    Args:
        httpserver: The pytest-httpserver fixture instance.
        path: The URL path to match (e.g., "/api/v1/resource").
        method: The HTTP method to match (e.g., "GET", "POST").
        response_data: The JSON data or raw string to return in the response body.
                       If None, an empty body is returned.
        status_code: The HTTP status code to return.
        response_headers: Optional dictionary of headers to return in the response.
        match_headers: Optional dictionary of headers that must be present in the request.
        match_query_string: Optional dictionary of query parameters that must be present.
        match_json: Optional JSON data that the request body must match.
        match_data: Optional raw string data that the request body must match.
        ordered: If True, ensures this expectation is met in the order it was defined
                 relative to other ordered expectations.
        **kwargs: Additional arguments passed directly to httpserver.expect_request.
                  See pytest-httpserver documentation for more advanced matching.
    """
    ...

def assert_request_received(
    httpserver: HTTPServer,
    path: str,
    method: str = "GET",
    expected_headers: Optional[Dict[str, str]] = None,
    expected_query: Optional[Dict[str, str]] = None,
    expected_json: Optional[Any] = None,
    expected_data: Optional[str] = None,
    count: Optional[int] = 1,
) -> None:
    """
    Asserts that specific requests were received by the mock server.

    Checks the server log for requests matching the criteria.

    Args:
        httpserver: The pytest-httpserver fixture instance.
        path: The expected URL path.
        method: The expected HTTP method.
        expected_headers: A dictionary of headers expected in the request. Checks for
                          presence and exact value match. Case-insensitive header keys.
        expected_query: A dictionary of query parameters expected. Checks for presence
                        and exact value match.
        expected_json: The expected JSON body of the request.
        expected_data: The expected raw string body of the request.
        count: The expected number of matching requests. If None, asserts at least one match.

    Raises:
        AssertionError: If the expected request(s) were not found in the server log.
    """
    ...
