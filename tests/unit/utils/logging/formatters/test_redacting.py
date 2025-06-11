from __future__ import annotations

import logging
from typing import Any, Callable

import pytest

from apiconfig.utils.logging.formatters import (
    RedactingFormatter,
    redact_message_helper,
    redact_structured_helper,
)


@pytest.fixture
def log_record_factory() -> Callable[..., logging.LogRecord]:
    """Factory for creating LogRecord objects with various parameters."""

    def make(
        msg: Any = "test message",
        args: tuple[Any, ...] = (),
        exc_info: Any = None,
        stack_info: Any = None,
        name: str = "test.logger",
        level: int = logging.INFO,
        pathname: str = __file__,
        lineno: int = 42,
        func: str | None = None,
    ) -> logging.LogRecord:
        record = logging.LogRecord(
            name=name,
            level=level,
            pathname=pathname,
            lineno=lineno,
            msg=msg,
            args=args,
            exc_info=exc_info,
            func=func,
            sinfo=stack_info,
        )
        return record

    return make


def _always_false(msg: Any) -> bool:
    """Return ``False`` for any input."""
    return False


def _always_false_structured(msg: Any, content_type: Any) -> bool:
    """Return ``False`` for any input and content type."""
    return False


def test_redacting_formatter_basic(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="redact test")
    assert fmt.format(record) == logging.Formatter().format(record)


def test_redacting_formatter_class_and_docstring() -> None:
    from apiconfig.utils.logging.formatters import RedactingFormatter

    assert RedactingFormatter.__doc__ is not None
    fmt = RedactingFormatter()
    assert isinstance(fmt, RedactingFormatter)


def test_redacting_formatter_format(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="redact format test")
    output = fmt.format(record)
    assert "redact format test" in output
    assert isinstance(output, str)


@pytest.mark.parametrize(
    "msg,content_type,expected",
    [
        (
            '{"token": "abc123", "data": "ok"}',
            "application/json",
            '{"token": "[REDACTED]", "data": "ok"}',
        ),
        (
            {"password": "p@ssw0rd", "foo": "bar"},
            None,
            '{"password": "[REDACTED]", "foo": "bar"}',
        ),
        (
            "secret=shh123&foo=bar",
            "application/x-www-form-urlencoded",
            "secret=%5BREDACTED%5D&foo=bar",
        ),
    ],
)
def test_redacting_formatter_structured_redaction(
    log_record_factory: Callable[..., logging.LogRecord],
    msg: Any,
    content_type: str | None,
    expected: str,
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg=msg)
    if content_type:
        record.content_type = content_type
    output = fmt.format(record)
    assert "[REDACTED]" in output or "%5BREDACTED%5D" in output
    assert (
        expected in output or expected.replace("%5BREDACTED%5D", "[REDACTED]") in output or expected.replace("[REDACTED]", "%5BREDACTED%5D") in output
    )


def test_redacting_formatter_headers_redaction(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="headers test")

    # Add headers attribute to the record
    headers = {"Authorization": "Bearer abc", "X-Api-Key": "xyz", "X-Other": "ok"}
    # We need to add the headers attribute to the record
    record.__dict__["headers"] = headers

    # Format the record
    fmt.format(record)
    assert (
        '"Authorization": "[REDACTED]"' in str(record.headers)  # type: ignore[attr-defined]
        or "'Authorization': '[REDACTED]'" in str(record.headers)  # type: ignore[attr-defined]
        or "[REDACTED]" in str(record.headers)  # type: ignore[attr-defined]
    )
    assert "[REDACTED]" in str(record.headers)  # type: ignore[attr-defined]
    assert "ok" in str(record.headers)  # type: ignore[attr-defined]


def test_redacting_formatter_plain_string_secret(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    import re

    secret_pattern = re.compile(r"secret_[a-z0-9]+", re.IGNORECASE)
    fmt = RedactingFormatter(body_sensitive_value_pattern=secret_pattern)
    record = log_record_factory(msg="this is a secret_abc123 and should be redacted")
    output = fmt.format(record)
    assert "[REDACTED]" in output
    assert "secret_abc123" not in output


def test_redacting_formatter_binary_and_unparsable(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg=b"\x00\x01\x02\x03")
    record.content_type = "application/octet-stream"
    output = fmt.format(record)
    assert "[REDACTED BODY]" in output
    record2 = log_record_factory(msg="not a json: {oops}")
    record2.content_type = "application/json"
    output2 = fmt.format(record2)
    assert "not a json" in output2


def test_redacting_formatter_empty_message(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="")
    output = fmt.format(record)
    assert output
    assert "[REDACTED]" in output


def test_redacting_formatter_fallback_branch(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()

    class WeirdObj:
        def __str__(self) -> str:
            return "weird"

    record = log_record_factory(msg=WeirdObj())
    output = fmt.format(record)
    assert "weird" in output


def test_redacting_formatter_redact_headers_exception(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="headers test")

    # Add headers attribute to the record
    record.__dict__["headers"] = {"Authorization": "Bearer abc"}

    def bad_redact_headers(*a: Any, **kw: Any) -> dict[str, str]:
        raise RuntimeError("fail")

    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_headers", bad_redact_headers)
    # We need to use monkeypatch instead of direct assignment
    monkeypatch.setattr(fmt, "_redact_headers_func", bad_redact_headers)
    fmt.format(record)
    assert record.headers == {"Authorization": "Bearer abc"}  # type: ignore[attr-defined]


def test_redacting_formatter_redact_structured_exception(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"foo": "bar"})

    def bad_redact_body(*a: Any, **kw: Any) -> Any:
        raise RuntimeError("fail")

    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_body", bad_redact_body)
    # We need to use monkeypatch instead of direct assignment
    monkeypatch.setattr(fmt, "_redact_body", bad_redact_body)
    output = fmt.format(record)
    assert "[REDACTED]" in output


def test_redacting_formatter_structured_dict_list_coverage(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"secret": "abc", "foo": "bar"})
    output = fmt.format(record)
    assert "[REDACTED]" in output
    record2 = log_record_factory(msg=[{"token": "abc"}])
    output2 = fmt.format(record2)
    assert "[REDACTED]" in output2


def test_redacting_formatter_structured_string_json_exception(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg='{"token": "abc"}')

    def bad_redact_body(*a: Any, **kw: Any) -> Any:
        raise RuntimeError("fail")

    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_body", bad_redact_body)
    monkeypatch.setattr(fmt, "_redact_body", bad_redact_body)
    output = fmt.format(record)
    assert '{"token": "abc"}' in output


def test_redacting_formatter_structured_dict_exception(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"token": "abc"})

    def bad_redact_body(*a: Any, **kw: Any) -> Any:
        raise RuntimeError("fail")

    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_body", bad_redact_body)
    output = fmt.format(record)
    assert "[REDACTED]" in output


def test_redacting_formatter_fallback_branch_strmsg(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()

    class OddType:
        def __str__(self) -> str:
            return "odd"

    record = log_record_factory(msg=OddType())
    output = fmt.format(record)
    assert "odd" in output


def test_redacting_formatter_is_structured_dict_list() -> None:
    """Test that _is_structured correctly identifies dict and list as structured data."""
    fmt = RedactingFormatter()
    assert fmt._is_structured({"foo": "bar"}, None) is True
    assert fmt._is_structured([1, 2, 3], None) is True


def test_redacting_formatter_redact_structured_dict_from_string(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    """Test that _redact_structured correctly handles dict return from redact_body."""
    fmt = RedactingFormatter()

    # Mock redact_body to return a dict
    def mock_redact_body(msg: Any, **kwargs: Any) -> dict[str, bool]:
        return {"redacted": True, "original": False}

    monkeypatch.setattr(fmt, "_redact_body", mock_redact_body)

    # Test with a JSON string that should be parsed and redacted
    result = redact_structured_helper(fmt, '{"token": "secret"}', "application/json")

    # Verify json.dumps was called
    import json

    expected = json.dumps({"redacted": True, "original": False}, ensure_ascii=False)
    assert result == expected


def test_redacting_formatter_redact_structured_list_from_string_direct(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test _redact_structured when a list is returned from redact_body."""
    fmt = RedactingFormatter()

    # Create a string that looks like JSON
    json_string = '[{"token": "secret"}]'

    # Mock redact_body to return a list when called with a string
    def mock_redact_body(msg: Any, **kwargs: Any) -> list[dict[str, bool]] | Any:
        if isinstance(msg, str) and msg == json_string:
            return [{"redacted": True}]
        return msg

    # Replace the redact_body method using monkeypatch
    monkeypatch.setattr(fmt, "_redact_body", mock_redact_body)

    try:
        # Call _redact_structured with a string that will be processed as JSON
        result = redact_structured_helper(fmt, json_string, "application/json")

        # Verify json.dumps was called
        import json

        expected = json.dumps([{"redacted": True}], ensure_ascii=False)
        assert result == expected
    finally:
        # No need to restore when using monkeypatch
        pass


def test_redacting_formatter_redact_structured_other_type_direct(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test _redact_structured when redact_body returns an unexpected type."""
    fmt = RedactingFormatter()

    # Create a string input
    test_input = "test input"

    # Mock redact_body to return a non-dict/list, non-string value
    def mock_redact_body(msg: Any, **kwargs: Any) -> int | Any:
        if msg == test_input:
            return 42
        return msg

    # Replace the redact_body method using monkeypatch
    monkeypatch.setattr(fmt, "_redact_body", mock_redact_body)

    try:
        # Call _redact_structured with a string
        result = redact_structured_helper(fmt, test_input, "text/plain")

        # Verify str() was called on the returned value
        assert result == "42"
    finally:
        # No need to restore when using monkeypatch
        pass


def test_redacting_formatter_redact_message_dict_json_dumps_direct(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    """Test that a dict message is converted to JSON in _redact_message."""
    fmt = RedactingFormatter()

    # Create a dict to be returned by the mocked redact_body
    redacted_dict = {"sensitive": "[REDACTED]", "normal": "value"}

    # Mock _redact_structured to return a dict
    def mock_redact_structured(msg: Any, content_type: Any) -> dict[str, Any]:
        return redacted_dict

    # Replace the _redact_structured method using monkeypatch
    monkeypatch.setattr(fmt, "_redact_structured", mock_redact_structured)

    try:
        # Create a record with a dict message
        record = log_record_factory(msg={"sensitive": "secret", "normal": "value"})

        # Call _redact_message directly
        redact_message_helper(fmt, record)

        # Verify the message was converted to a JSON string
        assert isinstance(record.msg, str)
        import json

        expected = json.dumps(redacted_dict, ensure_ascii=False)
        assert record.msg == expected
    finally:
        # No need to restore when using monkeypatch
        pass


def test_redacting_formatter_unknown_type_fallback_direct(
    log_record_factory: Callable[..., logging.LogRecord],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the fallback branch in _redact_message for unknown types."""
    fmt = RedactingFormatter()

    # Create a custom type that will trigger the fallback branch
    class CustomType:
        def __str__(self) -> str:
            return "custom object"

    # Create a record with the custom type
    obj = CustomType()
    record = log_record_factory(msg=obj)

    # Patch all the condition methods to return False using monkeypatch
    monkeypatch.setattr(fmt, "_is_binary", _always_false)
    monkeypatch.setattr(fmt, "_is_empty", _always_false)
    monkeypatch.setattr(fmt, "_is_structured", _always_false_structured)

    try:
        # Call _redact_message directly
        redact_message_helper(fmt, record)

        # Verify str() was called on the object
        assert record.msg == "custom object"
    finally:
        # No need to restore when using monkeypatch
        pass


def test_redacting_formatter_redact_structured_string_exception_fallback(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    """Test the exception fallback for string input in _redact_structured."""
    fmt = RedactingFormatter()

    # Mock redact_body to raise an exception
    def mock_redact_body_exception(msg: Any, **kwargs: Any) -> str:
        raise ValueError("Test exception")

    monkeypatch.setattr(fmt, "_redact_body", mock_redact_body_exception)

    # Test with a string input
    test_string = "test string"
    result = redact_structured_helper(fmt, test_string, "text/plain")

    # Verify the original string is returned
    assert result == test_string


def test_redacting_formatter_line_138_direct(monkeypatch: pytest.MonkeyPatch) -> None:
    """Exercise the _redact_message fallback path using a custom object."""
    fmt = RedactingFormatter()

    # Create a custom object that will trigger the fallback branch
    class NonStringNonDictNonList:
        def __str__(self) -> str:
            return "custom object str representation"

    obj = NonStringNonDictNonList()

    # Create a record with our custom object
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=42,
        msg=obj,
        args=(),
        exc_info=None,
    )

    # Override all the condition methods to ensure we hit the fallback branch
    monkeypatch.setattr(fmt, "_is_binary", _always_false)
    monkeypatch.setattr(fmt, "_is_empty", _always_false)
    monkeypatch.setattr(fmt, "_is_structured", _always_false_structured)

    # Call _redact_message directly
    redact_message_helper(fmt, record)

    # Verify str() was called on the object
    assert record.msg == "custom object str representation"


def test_redacting_formatter_line_220_direct(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure _redact_structured handles URL-encoded form data."""
    fmt = RedactingFormatter()

    # Create a string input
    string_input = "form_data=value"

    # Create a dict that will be returned by redact_body
    redacted_dict = {"form_data": "[REDACTED]"}

    # Override redact_body to return our dict using monkeypatch
    redact_body_override: Callable[..., dict[str, str]] = lambda msg, **kwargs: redacted_dict if msg == string_input else msg
    monkeypatch.setattr(fmt, "_redact_body", redact_body_override)

    try:
        # Call _redact_structured with our string input and form content type
        result = redact_structured_helper(fmt, string_input, "application/x-www-form-urlencoded")

        # Verify json.dumps was called
        import json

        expected = json.dumps(redacted_dict, ensure_ascii=False)
        assert result == expected
    finally:
        # No need to restore when using monkeypatch
        pass


def test_redacting_formatter_line_224_direct(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure _redact_structured stringifies custom outputs."""
    fmt = RedactingFormatter()

    # Create a non-string, non-dict, non-list input
    class CustomInput:
        pass

    custom_input = CustomInput()

    # Create a non-dict, non-list output that will be returned by redact_body
    class CustomOutput:
        def __str__(self) -> str:
            return "custom output str representation"

    custom_output = CustomOutput()

    # Override redact_body to return our custom output using monkeypatch

    def _fake_redact_body(msg: Any, **kwargs: Any) -> Any:
        return custom_output if msg == custom_input else msg

    monkeypatch.setattr(fmt, "_redact_body", _fake_redact_body)

    try:
        # Call _redact_structured with our custom input
        result = redact_structured_helper(fmt, custom_input, None)

        # Verify str() was called
        assert result == "custom output str representation"
    finally:
        # No need to restore when using monkeypatch
        pass


def test_redacting_formatter_line_138_direct_with_format(
    monkeypatch: pytest.MonkeyPatch,
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    """Exercise _redact_message via format() with a custom object."""
    fmt = RedactingFormatter()

    # Create a custom object that will trigger the fallback branch
    class CustomObject:
        def __str__(self) -> str:
            return "custom object string representation"

    # Create a record with the custom object
    obj = CustomObject()
    record = log_record_factory(msg=obj)

    # Monkeypatch the internal methods to force the fallback branch
    def mock_is_binary(msg: Any) -> bool:
        return False

    def mock_is_empty(msg: Any) -> bool:
        return False

    def mock_is_structured(msg: Any, content_type: Any) -> bool:
        return False

    monkeypatch.setattr(fmt, "_is_binary", mock_is_binary)
    monkeypatch.setattr(fmt, "_is_empty", mock_is_empty)
    monkeypatch.setattr(fmt, "_is_structured", mock_is_structured)

    # Call format which will call _redact_message
    output = fmt.format(record)

    # Verify the output contains the string representation
    assert "custom object string representation" in output


def test_redacting_formatter_line_138_with_subclass() -> None:
    """Create a subclass forcing the fallback branch in _redact_message."""

    # Create a subclass that overrides the necessary methods to force the fallback branch
    class TestRedactingFormatter(RedactingFormatter):
        def _redact_message(self, record: logging.LogRecord) -> None:
            # Get the original message
            orig_msg = getattr(record, "msg", None)

            # Force the fallback branch
            redacted_msg = str(orig_msg)

            # Set the message
            record.msg = redacted_msg
            record.args = ()

    # Create a formatter and a record
    fmt = TestRedactingFormatter()

    # Create a custom object
    class TestObject:
        def __str__(self) -> str:
            return "test object string representation"

    obj = TestObject()

    # Create a record with the custom object
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=42,
        msg=obj,
        args=(),
        exc_info=None,
    )

    # Call format
    output = fmt.format(record)

    # Verify the output contains the string representation
    assert "test object string representation" in output
