import logging
import sys
import traceback
from typing import Any, Callable, Literal, cast

import pytest

from apiconfig.utils.logging.formatters import DetailedFormatter, RedactingFormatter


class TypedLogRecord(logging.LogRecord):
    headers: dict[str, str]


@pytest.fixture
def log_record_factory() -> Callable[..., logging.LogRecord]:
    """Factory for creating LogRecord objects with various parameters."""
    def make(
        msg: str = "test message",
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


@pytest.mark.parametrize(
    "msg,expected_in",
    [
        ("simple message", "simple message"),
        ("multi\nline\nmessage", "multi\n"),
    ],
)
def test_detailed_formatter_basic_and_multiline(
    log_record_factory: Callable[..., logging.LogRecord],
    msg: str,
    expected_in: str
) -> None:
    fmt = DetailedFormatter()
    record = log_record_factory(msg=msg)
    output = fmt.format(record)
    # The message should appear in the output, and for multi-line, newlines should be present
    assert expected_in in output
    # The file/line info should always be present
    assert f"({__file__.split('/')[-1]}:42)" in output


def test_detailed_formatter_custom_format(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    custom_fmt = "[%(levelname)s] %(message)s"
    fmt = DetailedFormatter(fmt=custom_fmt)
    record = log_record_factory(msg="custom format test")
    output = fmt.format(record)
    assert "[INFO]" in output
    assert "custom format test" in output


def test_detailed_formatter_indents_multiline_message(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    msg = "first line\nsecond line\nthird line"
    fmt = DetailedFormatter()
    record = log_record_factory(msg=msg)
    output = fmt.format(record)
    # All lines should appear, and subsequent lines should be indented
    lines = output.splitlines()
    assert "first line" in lines[0]
    # At least one subsequent line should be indented (starts with spaces)
    assert any(line.startswith(" ") and "second line" in line for line in lines[1:])


def test_detailed_formatter_with_exception(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = DetailedFormatter()
    try:
        raise ValueError("fail!")
    except ValueError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="error occurred", exc_info=exc_info)
        output = fmt.format(record)
        # Exception text should be present and indented
        assert "ValueError: fail!" in output
        # Should be indented
        exc_lines = [line for line in output.splitlines() if "ValueError: fail!" in line]
        assert all(line.startswith("    ") for line in exc_lines)


def test_detailed_formatter_with_stack_info(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = DetailedFormatter()
    stack = "".join(traceback.format_stack())
    record = log_record_factory(msg="with stack", stack_info=stack)
    output = fmt.format(record)
    # Stack info should be present and indented
    assert "with stack" in output
    assert "File" in output  # Should contain a stack frame
    stack_lines = [line for line in output.splitlines() if "File" in line]
    assert all(line.startswith("    ") for line in stack_lines)


def test_detailed_formatter_with_exception_and_stack(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = DetailedFormatter()
    stack = "".join(traceback.format_stack())
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="both", exc_info=exc_info, stack_info=stack)
        output = fmt.format(record)
        # Both exception and stack info should be present and indented
        assert "RuntimeError: boom" in output
        assert "File" in output
        # Exception and stack should be indented
        exc_lines = [line for line in output.splitlines() if "RuntimeError: boom" in line]
        stack_lines = [line for line in output.splitlines() if "File" in line]
        assert all(line.startswith("    ") for line in exc_lines)
        assert all(line.startswith("    ") for line in stack_lines)


def test_detailed_formatter_exc_info_and_stack_full_branch(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers both exc_info (with exc_text unset) and stack_info branches for 100% coverage."""
    fmt = DetailedFormatter()
    stack = "".join(traceback.format_stack())
    try:
        raise OSError("full branch test")
    except OSError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="exc and stack", exc_info=exc_info, stack_info=stack)
        # exc_text should not be set yet
        if hasattr(record, "exc_text"):
            delattr(record, "exc_text")
        output = fmt.format(record)
        # Both exception and stack info should be present and indented
        assert "OSError: full branch test" in output
        assert "File" in output
        exc_lines = [line for line in output.splitlines() if "OSError: full branch test" in line]
        stack_lines = [line for line in output.splitlines() if "File" in line]
        assert all(line.startswith("    ") for line in exc_lines)
        assert all(line.startswith("    ") for line in stack_lines)


@pytest.mark.parametrize("style", ["%"])
def test_detailed_formatter_style_variants(
    log_record_factory: Callable[..., logging.LogRecord], style: str
) -> None:
    fmt = DetailedFormatter(style=cast(Literal["%"], style))
    record = log_record_factory(msg="style test")
    output = fmt.format(record)
    assert "style test" in output


def test_detailed_formatter_repr_and_str(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = DetailedFormatter()
    record = log_record_factory(msg="repr test")
    output = fmt.format(record)
    # __str__ and __repr__ are inherited, just check output is string
    assert isinstance(output, str)


def test_redacting_formatter_basic(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="redact test")
    # Should behave like default Formatter
    assert fmt.format(record) == logging.Formatter().format(record)


def test_detailed_formatter_empty_message(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = DetailedFormatter()
    record = log_record_factory(msg="")
    output = fmt.format(record)
    assert isinstance(output, str)
    assert output  # Should still produce a string, possibly with just metadata


def test_redacting_formatter_class_and_docstring() -> None:
    """Covers RedactingFormatter class definition and docstring for coverage."""
    from apiconfig.utils.logging.formatters import RedactingFormatter
    assert RedactingFormatter.__doc__ is not None
    fmt = RedactingFormatter()
    assert isinstance(fmt, RedactingFormatter)


def test_redacting_formatter_format(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers RedactingFormatter.format for coverage of class body and inherited method."""
    fmt = RedactingFormatter()
    record = log_record_factory(msg="redact format test")
    output = fmt.format(record)
    assert "redact format test" in output
    assert isinstance(output, str)


@pytest.mark.parametrize(
    "msg,content_type,expected",
    [
        ("{\"token\": \"abc123\", \"data\": \"ok\"}", "application/json", '{"token": "[REDACTED]", "data": "ok"}'),
        ({"password": "p@ssw0rd", "foo": "bar"}, None, '{"password": "[REDACTED]", "foo": "bar"}'),
        ("secret=shh123&foo=bar", "application/x-www-form-urlencoded", "secret=%5BREDACTED%5D&foo=bar"),
    ]
)
def test_redacting_formatter_structured_redaction(
    log_record_factory: Callable[..., logging.LogRecord],
    msg: Any,
    content_type: str | None,
    expected: str
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg=msg)
    if content_type:
        record.content_type = content_type
    output = fmt.format(record)
    # Accept both [REDACTED] and %5BREDACTED%5D for form-encoded, and ensure the expected output is present
    assert "[REDACTED]" in output or "%5BREDACTED%5D" in output
    assert (
        expected in output
        or expected.replace("%5BREDACTED%5D", "[REDACTED]") in output
        or expected.replace("[REDACTED]", "%5BREDACTED%5D") in output
    )


def test_redacting_formatter_headers_redaction(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="headers test")
    from typing import cast
    setattr(record, "headers", {"Authorization": "Bearer abc", "X-Api-Key": "xyz", "X-Other": "ok"})
    record = cast(TypedLogRecord, record)
    fmt.format(record)
    # Accept both JSON and dict string representations
    assert (
        '"Authorization": "[REDACTED]"' in str(record.headers)
        or "'Authorization': '[REDACTED]'" in str(record.headers)
        or "[REDACTED]" in str(record.headers)
    )
    assert "[REDACTED]" in str(record.headers)
    assert "ok" in str(record.headers)


def test_redacting_formatter_plain_string_secret(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    import re
    secret_pattern = re.compile(r"secret_[a-z0-9]+", re.IGNORECASE)
    fmt = RedactingFormatter(body_sensitive_value_pattern=secret_pattern)
    record = log_record_factory(msg="this is a secret_abc123 and should be redacted")
    output = fmt.format(record)
    assert "[REDACTED]" in output
    assert "secret_abc123" not in output


def test_redacting_formatter_binary_and_unparsable(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    # Binary data
    record = log_record_factory(msg=b"\x00\x01\x02\x03")
    record.content_type = "application/octet-stream"
    output = fmt.format(record)
    assert "[REDACTED BODY]" in output
    # Unparsable string
    record2 = log_record_factory(msg="not a json: {oops}")
    record2.content_type = "application/json"
    output2 = fmt.format(record2)
    assert "not a json" in output2


def test_redacting_formatter_empty_message(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="")
    output = fmt.format(record)
    assert output
    assert "[REDACTED]" in output


def test_detailed_formatter_metadata_len_minus_one(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers the case where metadata_len == -1 in DetailedFormatter (multi-line message, no %(message)s in format)."""
    # Custom format string that puts %(message)s on the second line only
    custom_fmt = "%(asctime)s [%(levelname)s] [%(name)s]\n%(message)s"
    fmt = DetailedFormatter(fmt=custom_fmt)
    # Multi-line message will not appear in the formatted output's first line
    msg = "should not be found\nsecond line"
    record = log_record_factory(msg=msg)
    output = fmt.format(record)
    # The message should not be in the first line, so metadata_len == -1 is triggered
    # Both lines of the message should appear in the output, and the second should be indented
    assert "should not be found" in output
    assert "second line" in output
    lines = output.splitlines()
    # The first line should not contain the message
    assert "should not be found" not in lines[0]
    # The second line should be the first line of the message, indented
    assert lines[1].lstrip() == "should not be found"
    assert lines[1].startswith(" ")
    # The third line should be the indented second line of the message
    assert lines[2].lstrip() == "second line" and lines[2].startswith(" ")
    assert isinstance(output, str)
    assert output  # Output should not be empty


def test_detailed_formatter_exc_info_sets_exc_text(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers the case where exc_info is set and exc_text is explicitly None, triggering the branch for 100% coverage."""
    fmt = DetailedFormatter()
    try:
        raise KeyError("trigger exc_info path")
    except KeyError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="exception path", exc_info=exc_info)
        # Explicitly set exc_text to None to guarantee coverage of the branch
        record.exc_text = None
        output = fmt.format(record)
        # exc_text should now be set and present in the output
        assert "KeyError: 'trigger exc_info path'" in output


def test_redacting_formatter_fallback_branch(
    log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers the fallback branch in _redact_message (msg is not str, dict, list, or bytes)."""
    fmt = RedactingFormatter()

    class WeirdObj:
        def __str__(self) -> str:
            return "weird"
    record = log_record_factory(msg=WeirdObj())
    output = fmt.format(record)
    assert "weird" in output


def test_redacting_formatter_redact_headers_exception(
    monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers the exception branch in _redact_headers."""
    fmt = RedactingFormatter()
    record = log_record_factory(msg="headers test")
    from typing import cast
    setattr(record, "headers", {"Authorization": "Bearer abc"})
    record = cast(TypedLogRecord, record)

    def bad_redact_headers(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_headers", bad_redact_headers)
    fmt.format(record)
    # Should not raise, and headers should remain unchanged
    assert record.headers == {"Authorization": "Bearer abc"}


def test_redacting_formatter_redact_structured_exception(
    monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    """Covers the exception branch in _redact_structured."""
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"foo": "bar"})

    def bad_redact_body(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_body", bad_redact_body)
    output = fmt.format(record)
    assert "[REDACTED]" in output

# --- Additional tests for 100% coverage of RedactingFormatter ---


def test_redacting_formatter_structured_dict_list_coverage(log_record_factory: Callable[..., logging.LogRecord]) -> None:
    """Covers _is_structured (dict/list), _redact_structured (dict/list), and fallback branches."""
    fmt = RedactingFormatter()
    # dict input triggers _is_structured True at line 223 and dict/list serialization at 209-210, 264, 284
    record = log_record_factory(msg={"secret": "abc", "foo": "bar"})
    output = fmt.format(record)
    assert "[REDACTED]" in output
    # list input triggers same path
    record2 = log_record_factory(msg=[{"token": "abc"}])
    output2 = fmt.format(record2)
    assert "[REDACTED]" in output2


def test_redacting_formatter_structured_string_json_exception(monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]) -> None:
    """Covers the exception branch in _redact_structured for string input (lines 266-268, 292)."""
    fmt = RedactingFormatter()
    record = log_record_factory(msg='{"token": "abc"}')
    # Patch redact_body to raise

    def bad_redact_body(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_body", bad_redact_body)
    output = fmt.format(record)
    assert '{"token": "abc"}' in output  # Should fall back to original string


def test_redacting_formatter_structured_dict_exception(monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]) -> None:
    """Covers the exception branch in _redact_structured for dict/list input (lines 288, 293)."""
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"token": "abc"})

    def bad_redact_body(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr("apiconfig.utils.logging.formatters.redact_body", bad_redact_body)
    output = fmt.format(record)
    assert "[REDACTED]" in output


def test_redacting_formatter_fallback_branch_strmsg(log_record_factory: Callable[..., logging.LogRecord]) -> None:
    """Covers fallback branch in _redact_message (line 204) for a custom object not handled by other branches."""
    fmt = RedactingFormatter()

    class OddType:
        def __str__(self) -> str:
            return "odd"
    record = log_record_factory(msg=OddType())
    output = fmt.format(record)
    assert "odd" in output


def test_detailed_formatter_exc_info_sets_exc_text_branch(log_record_factory: Callable[..., logging.LogRecord]) -> None:
    """Covers line 69: record.exc_text = self.formatException(record.exc_info)"""
    fmt = DetailedFormatter()
    try:
        raise KeyError("trigger exc_info path")
    except KeyError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="exception path", exc_info=exc_info)
        # exc_text is not set, so formatException should be called
        if hasattr(record, "exc_text"):
            delattr(record, "exc_text")
        output = fmt.format(record)
        assert "KeyError: 'trigger exc_info path'" in output
