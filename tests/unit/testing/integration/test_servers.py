"""Tests for the integration testing servers module."""

import json
from unittest.mock import MagicMock

import pytest
from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Request, Response

from apiconfig.testing.integration.servers import (
    assert_request_received,
    configure_mock_response,
)


class TestConfigureMockResponse:
    """Tests for the configure_mock_response function."""

    def test_configure_mock_response_basic(self) -> None:
        """Test configure_mock_response with basic parameters."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data={"result": "success"},
            status_code=200,
        )

        # Check that expect_request was called correctly
        mock_httpserver.expect_request.assert_called_once_with(uri="/test", method="GET", ordered=False)

        # Check that respond_with_response was called correctly
        mock_expectation.respond_with_response.assert_called_once()
        args, kwargs = mock_expectation.respond_with_response.call_args

        # Check the response object
        response_obj = args[0]
        assert isinstance(response_obj, Response)
        assert response_obj.status_code == 200
        assert response_obj.headers["Content-Type"] == "application/json"

        # Check the response_json kwarg
        assert "response_json" in kwargs
        assert kwargs["response_json"] == {"result": "success"}

    def test_configure_mock_response_with_string_response(self) -> None:
        """Test configure_mock_response with a string response."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with a string response
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data="Hello, world!",
            status_code=200,
        )

        # Check that respond_with_response was called with response_data
        mock_expectation.respond_with_response.assert_called_once()
        args, kwargs = mock_expectation.respond_with_response.call_args

        assert "response_data" in kwargs
        assert kwargs["response_data"] == "Hello, world!"

    def test_configure_mock_response_with_none_response(self) -> None:
        """Test configure_mock_response with None response."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with None response
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data=None,
            status_code=204,
        )

        # Check that respond_with_response was called without response_data or response_json
        mock_expectation.respond_with_response.assert_called_once()
        args, kwargs = mock_expectation.respond_with_response.call_args

        assert "response_data" not in kwargs
        assert "response_json" not in kwargs

    def test_configure_mock_response_with_custom_headers(self) -> None:
        """Test configure_mock_response with custom response headers."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with custom headers
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data={"result": "success"},
            status_code=200,
            response_headers={"X-Custom-Header": "test_value"},
        )

        # Check that respond_with_response was called with the custom headers
        mock_expectation.respond_with_response.assert_called_once()
        args, kwargs = mock_expectation.respond_with_response.call_args

        response_obj = args[0]
        assert response_obj.headers["X-Custom-Header"] == "test_value"
        assert response_obj.headers["Content-Type"] == "application/json"

    def test_configure_mock_response_with_match_headers(self) -> None:
        """Test configure_mock_response with match_headers."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with match_headers
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data={"result": "success"},
            match_headers={"Authorization": "Bearer token"},
        )

        # Check that expect_request was called with the headers
        mock_httpserver.expect_request.assert_called_once_with(
            uri="/test",
            method="GET",
            ordered=False,
            headers={"Authorization": "Bearer token"},
        )

    def test_configure_mock_response_with_match_query_string(self) -> None:
        """Test configure_mock_response with match_query_string."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with match_query_string
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data={"result": "success"},
            match_query_string={"page": "1", "limit": "10"},
        )

        # Check that expect_request was called with the query string
        mock_httpserver.expect_request.assert_called_once_with(uri="/test", method="GET", ordered=False, query_string="page=1&limit=10")

    def test_configure_mock_response_with_match_json(self) -> None:
        """Test configure_mock_response with match_json."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with match_json
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="POST",
            response_data={"result": "success"},
            match_json={"name": "test"},
        )

        # Check that expect_request was called with the json
        mock_httpserver.expect_request.assert_called_once_with(uri="/test", method="POST", ordered=False, json={"name": "test"})

    def test_configure_mock_response_with_match_data(self) -> None:
        """Test configure_mock_response with match_data."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with match_data
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="POST",
            response_data={"result": "success"},
            match_data="name=test",
        )

        # Check that expect_request was called with the data
        mock_httpserver.expect_request.assert_called_once_with(uri="/test", method="POST", ordered=False, data="name=test")

    def test_configure_mock_response_with_ordered(self) -> None:
        """Test configure_mock_response with ordered=True."""
        # Create a mock HTTPServer
        mock_httpserver = MagicMock(spec=HTTPServer)
        mock_expectation = MagicMock()
        mock_httpserver.expect_request.return_value = mock_expectation

        # Call the function with ordered=True
        configure_mock_response(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            response_data={"result": "success"},
            ordered=True,
        )

        # Check that expect_request was called with ordered=True
        mock_httpserver.expect_request.assert_called_once_with(uri="/test", method="GET", ordered=True)


class TestAssertRequestReceived:
    """Tests for the assert_request_received function."""

    def test_assert_request_received_basic(self) -> None:
        """Test assert_request_received with basic parameters."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {}
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function
        assert_request_received(httpserver=mock_httpserver, path="/test", method="GET")

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_with_expected_headers(self) -> None:
        """Test assert_request_received with expected headers."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with headers
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer token",
        }
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with expected headers
        assert_request_received(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            expected_headers={"Content-Type": "application/json"},
        )

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_with_case_insensitive_headers(self) -> None:
        """Test assert_request_received with case-insensitive header matching."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with headers
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {"content-type": "application/json"}
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with expected headers in different case
        assert_request_received(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            expected_headers={"Content-Type": "application/json"},
        )

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_with_expected_query(self) -> None:
        """Test assert_request_received with expected query parameters."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with query parameters
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {}
        mock_request.args = {"page": "1", "limit": "10"}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with expected query parameters
        assert_request_received(
            httpserver=mock_httpserver,
            path="/test",
            method="GET",
            expected_query={"page": "1"},
        )

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_with_expected_json(self) -> None:
        """Test assert_request_received with expected JSON body."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with JSON body
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "POST"
        mock_request.headers = {"Content-Type": "application/json"}
        mock_request.args = {}
        mock_request.get_data.return_value = json.dumps({"name": "test", "value": 123})

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with expected JSON
        assert_request_received(
            httpserver=mock_httpserver,
            path="/test",
            method="POST",
            expected_json={"name": "test", "value": 123},
        )

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_with_expected_data(self) -> None:
        """Test assert_request_received with expected raw data body."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with raw data body
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "POST"
        mock_request.headers = {"Content-Type": "text/plain"}
        mock_request.args = {}
        mock_request.get_data.return_value = "Hello, world!"

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with expected data
        assert_request_received(
            httpserver=mock_httpserver,
            path="/test",
            method="POST",
            expected_data="Hello, world!",
        )

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_no_matching_requests(self) -> None:
        """Test assert_request_received raises when no matching requests are found."""
        # Create a mock HTTPServer with a log entry for a different path
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/other"
        mock_request.method = "GET"
        mock_request.headers = {}
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function and expect it to raise
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(httpserver=mock_httpserver, path="/test", method="GET")

    def test_assert_request_received_with_count(self) -> None:
        """Test assert_request_received with count parameter."""
        # Create a mock HTTPServer with multiple log entries
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create mock requests
        mock_request1 = MagicMock(spec=Request)
        mock_request1.path = "/test"
        mock_request1.method = "GET"
        mock_request1.headers = {}
        mock_request1.args = {}

        mock_request2 = MagicMock(spec=Request)
        mock_request2.path = "/test"
        mock_request2.method = "GET"
        mock_request2.headers = {}
        mock_request2.args = {}

        # Create mock responses
        mock_response1 = MagicMock()
        mock_response2 = MagicMock()

        # Set up the log with the requests and responses
        mock_httpserver.log = [
            (mock_request1, mock_response1),
            (mock_request2, mock_response2),
        ]

        # Call the function with count=2
        assert_request_received(httpserver=mock_httpserver, path="/test", method="GET", count=2)

        # No assertion needed - if the function doesn't raise, it passed

        # Call the function with count=1 and expect it to raise
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(httpserver=mock_httpserver, path="/test", method="GET", count=1)

    def test_assert_request_received_with_none_count(self) -> None:
        """Test assert_request_received with count=None."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {}
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with count=None
        assert_request_received(httpserver=mock_httpserver, path="/test", method="GET", count=None)

        # No assertion needed - if the function doesn't raise, it passed

    def test_assert_request_received_header_mismatch(self) -> None:
        """Test assert_request_received when headers don't match."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with different headers
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {"Content-Type": "text/plain"}
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with different expected headers
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(
                httpserver=mock_httpserver,
                path="/test",
                method="GET",
                expected_headers={"Content-Type": "application/json"},
            )

    def test_assert_request_received_query_mismatch(self) -> None:
        """Test assert_request_received when query parameters don't match."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with different query parameters
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "GET"
        mock_request.headers = {}
        mock_request.args = {"page": "2"}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with different expected query parameters
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(
                httpserver=mock_httpserver,
                path="/test",
                method="GET",
                expected_query={"page": "1"},
            )

    def test_assert_request_received_json_mismatch(self) -> None:
        """Test assert_request_received when JSON body doesn't match."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with different JSON body
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "POST"
        mock_request.headers = {"Content-Type": "application/json"}
        mock_request.args = {}
        mock_request.get_data.return_value = json.dumps({"name": "different", "value": 456})

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with different expected JSON
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(
                httpserver=mock_httpserver,
                path="/test",
                method="POST",
                expected_json={"name": "test", "value": 123},
            )

    def test_assert_request_received_invalid_json(self) -> None:
        """Test assert_request_received when request body is not valid JSON."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with invalid JSON body
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "POST"
        mock_request.headers = {"Content-Type": "application/json"}
        mock_request.args = {}
        mock_request.get_data.return_value = "invalid json"

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with expected JSON
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(
                httpserver=mock_httpserver,
                path="/test",
                method="POST",
                expected_json={"name": "test"},
            )

    def test_assert_request_received_data_mismatch(self) -> None:
        """Test assert_request_received when raw data body doesn't match."""
        # Create a mock HTTPServer with a log entry
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request with different raw data body
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/test"
        mock_request.method = "POST"
        mock_request.headers = {"Content-Type": "text/plain"}
        mock_request.args = {}
        mock_request.get_data.return_value = "Different data"

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with different expected data
        with pytest.raises(AssertionError, match="Expected 1 request"):
            assert_request_received(
                httpserver=mock_httpserver,
                path="/test",
                method="POST",
                expected_data="Hello, world!",
            )

    def test_assert_request_received_with_none_count_no_matches(self) -> None:
        """Test assert_request_received with count=None when no requests match."""
        # Create a mock HTTPServer with a log entry for a different path
        mock_httpserver = MagicMock(spec=HTTPServer)

        # Create a mock request
        mock_request = MagicMock(spec=Request)
        mock_request.path = "/other"
        mock_request.method = "GET"
        mock_request.headers = {}
        mock_request.args = {}

        # Create a mock response
        mock_response = MagicMock()

        # Set up the log with the request and response
        mock_httpserver.log = [(mock_request, mock_response)]

        # Call the function with count=None and expect it to raise
        with pytest.raises(AssertionError, match="Expected at least one request"):
            assert_request_received(httpserver=mock_httpserver, path="/test", method="GET", count=None)
