# -*- coding: utf-8 -*-
# mypy: ignore-errors
# flake8: noqa
"""
Type stubs for mock API server utilities.
"""
from typing import Any, Dict, Optional, Union

from pytest_httpserver import HTTPServer
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
    ...
