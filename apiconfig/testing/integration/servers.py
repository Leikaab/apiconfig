# apiconfig/testing/integration/servers.py
# -*- coding: utf-8 -*-
"""Implementation of mock API server utilities for integration testing."""
import json
from typing import Any, Dict, Optional, Union

from pytest_httpserver import HTTPServer  # type: ignore[import-untyped]
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
    """Configure mock response for integration testing."""
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

    expectation = httpserver.expect_request(uri=path, method=method, ordered=ordered, **expect_kwargs)
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
    """Assert that specific requests were received by the mock server."""
    matching_requests = []
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
