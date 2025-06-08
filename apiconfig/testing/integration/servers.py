# apiconfig/testing/integration/servers.py
# -*- coding: utf-8 -*-
"""
Mock API server utilities for integration testing.

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
import json
from typing import Any, Dict, List, Optional, Tuple, Union

from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Request, Response


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
    """Configure a specific response expectation for the mock HTTPServer.

    This function allows detailed matching of incoming requests, making it suitable
    for testing various authentication strategies, including custom ones that
    might add specific headers, query parameters, or body content.

    For stateful authentication flows (e.g., challenge-response), call this
    function multiple times in the expected order of requests, setting `ordered=True`.

    Parameters
    ----------
    httpserver : HTTPServer
        The pytest-httpserver fixture instance.
    path : str
        The URL path to match (e.g., "/api/v1/resource").
    method : str, default "GET"
        The HTTP method to match (e.g., "GET", "POST").
    response_data : Optional[Union[Dict[str, Any], str]], default None
        The JSON data or raw string to return in the response body.
        If None, an empty body is returned.
    status_code : int, default 200
        The HTTP status code to return.
    response_headers : Optional[Dict[str, str]], default None
        Optional dictionary of headers to return in the response.
    match_headers : Optional[Dict[str, str]], default None
        Optional dictionary of headers that must be present in the request.
    match_query_string : Optional[Dict[str, str]], default None
        Optional dictionary of query parameters that must be present.
    match_json : Optional[Any], default None
        Optional JSON data that the request body must match.
    match_data : Optional[str], default None
        Optional raw string data that the request body must match.
    ordered : bool, default False
        If True, ensures this expectation is met in the order it was defined
        relative to other ordered expectations.
    **kwargs : Any
        Additional arguments passed directly to httpserver.expect_request.
        See pytest-httpserver documentation for more advanced matching.

    Returns
    -------
    None
    """
    if response_headers is None:
        response_headers = {}

    # Default content type if response_data is a dict (implying JSON)
    if isinstance(response_data, dict) and "Content-Type" not in response_headers:
        response_headers["Content-Type"] = "application/json"

    # Prepare matching arguments for expect_request
    expect_kwargs = kwargs.copy()
    if match_headers:
        expect_kwargs["headers"] = match_headers
    if match_query_string:
        # pytest-httpserver expects query_string as bytes or str
        expect_kwargs["query_string"] = "&".join(f"{k}={v}" for k, v in match_query_string.items())
    if match_json:
        expect_kwargs["json"] = match_json
    if match_data:
        expect_kwargs["data"] = match_data

    # pytest-httpserver expects response_json for dicts and response_data for strings
    response_kwargs: Dict[str, Any] = {}
    if isinstance(response_data, dict):
        response_kwargs["response_json"] = response_data
    elif isinstance(response_data, str):
        response_kwargs["response_data"] = response_data
    # Handle None case implicitly (empty body)

    # Pass 'ordered' for test compatibility; type: ignore needed for real HTTPServer
    expectation = httpserver.expect_request(uri=path, method=method, ordered=ordered, **expect_kwargs)  # type: ignore[call-arg]
    expectation.respond_with_response(Response(status=status_code, headers=response_headers), **response_kwargs)


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
    """Assert that specific requests were received by the mock server.

    Checks the server log for requests matching the criteria.

    Parameters
    ----------
    httpserver : HTTPServer
        The pytest-httpserver fixture instance.
    path : str
        The expected URL path.
    method : str, default "GET"
        The expected HTTP method.
    expected_headers : Optional[Dict[str, str]], default None
        A dictionary of headers expected in the request. Checks for
        presence and exact value match. Case-insensitive header keys.
    expected_query : Optional[Dict[str, str]], default None
        A dictionary of query parameters expected. Checks for presence
        and exact value match.
    expected_json : Optional[Any], default None
        The expected JSON body of the request.
    expected_data : Optional[str], default None
        The expected raw string body of the request.
    count : Optional[int], default 1
        The expected number of matching requests. If None, asserts at least one match.

    Raises
    ------
    AssertionError
        If the expected request(s) were not found in the server log.
    """
    matching_requests: List[Tuple[Request, Response]] = []
    lower_expected_headers = {k.lower(): v for k, v in expected_headers.items()} if expected_headers else None

    log = httpserver.log
    for entry in log:
        request: Request = entry[0]  # entry is a tuple (request, response)
        if request.path == path and request.method == method:
            match = True
            # Check headers
            if lower_expected_headers:
                request_headers_lower = {k.lower(): v for k, v in request.headers.items()}
                if not all(item in request_headers_lower.items() for item in lower_expected_headers.items()):
                    match = False
            # Check query parameters
            if expected_query and match:
                if not all(item in request.args.items() for item in expected_query.items()):
                    match = False
            # Check JSON body
            if expected_json is not None and match:
                try:
                    request_json = json.loads(request.get_data(as_text=True))
                    if request_json != expected_json:
                        match = False
                except json.JSONDecodeError:
                    match = False
            # Check raw data body
            elif expected_data is not None and match:
                if request.get_data(as_text=True) != expected_data:
                    match = False

            if match:
                matching_requests.append(entry)

    if count is not None:
        assert len(matching_requests) == count, (
            f"Expected {count} request(s) matching criteria for {method} {path}, " f"but found {len(matching_requests)}. Log: {log}"
        )
    else:
        assert len(matching_requests) > 0, f"Expected at least one request matching criteria for {method} {path}, " f"but found none. Log: {log}"
