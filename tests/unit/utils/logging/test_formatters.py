import logging
import sys
import traceback
from typing import Any, Callable, Literal, cast

import pytest

from apiconfig.utils.logging.formatters import DetailedFormatter, RedactingFormatter


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
