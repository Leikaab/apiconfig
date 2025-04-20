import logging
import sys
import traceback
from typing import Any, Callable

import pytest

from apiconfig.utils.logging.formatters import DetailedFormatter


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
    log_record_factory: Callable[..., logging.LogRecord], msg: str, expected_in: str
) -> None:
    fmt = DetailedFormatter()
    record = log_record_factory(msg=msg)
    output = fmt.format(record)
    assert expected_in in output
    assert f"({__file__.split('/')[-1]}:42)" in output


def test_detailed_formatter_custom_format(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    custom_fmt = "[%(levelname)s] %(message)s"
    fmt = DetailedFormatter(fmt=custom_fmt)
    record = log_record_factory(msg="custom format test")
    output = fmt.format(record)
    assert "[INFO]" in output
    assert "custom format test" in output


def test_detailed_formatter_indents_multiline_message(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    msg = "first line\nsecond line\nthird line"
    fmt = DetailedFormatter()
    record = log_record_factory(msg=msg)
    output = fmt.format(record)
    lines = output.splitlines()
    assert "first line" in lines[0]
    assert any(line.startswith(" ") and "second line" in line for line in lines[1:])


def test_detailed_formatter_with_exception(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    try:
        raise ValueError("fail!")
    except ValueError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="error occurred", exc_info=exc_info)
        output = fmt.format(record)
        assert "ValueError: fail!" in output
        exc_lines = [
            line for line in output.splitlines() if "ValueError: fail!" in line
        ]
        assert all(line.startswith("    ") for line in exc_lines)


def test_detailed_formatter_with_stack_info(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    stack = "".join(traceback.format_stack())
    record = log_record_factory(msg="with stack", stack_info=stack)
    output = fmt.format(record)
    assert "with stack" in output
    assert "File" in output
    stack_lines = [line for line in output.splitlines() if "File" in line]
    assert all(line.startswith("    ") for line in stack_lines)


def test_detailed_formatter_with_exception_and_stack(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    stack = "".join(traceback.format_stack())
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="both", exc_info=exc_info, stack_info=stack)
        output = fmt.format(record)
        assert "RuntimeError: boom" in output
        assert "File" in output
        exc_lines = [
            line for line in output.splitlines() if "RuntimeError: boom" in line
        ]
        stack_lines = [line for line in output.splitlines() if "File" in line]
        assert all(line.startswith("    ") for line in exc_lines)
        assert all(line.startswith("    ") for line in stack_lines)


def test_detailed_formatter_exc_info_and_stack_full_branch(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    stack = "".join(traceback.format_stack())
    try:
        raise OSError("full branch test")
    except OSError:
        exc_info = sys.exc_info()
        record = log_record_factory(
            msg="exc and stack", exc_info=exc_info, stack_info=stack
        )
        if hasattr(record, "exc_text"):
            delattr(record, "exc_text")
        output = fmt.format(record)
        assert "OSError: full branch test" in output
        assert "File" in output
        exc_lines = [
            line for line in output.splitlines() if "OSError: full branch test" in line
        ]
        stack_lines = [line for line in output.splitlines() if "File" in line]
        assert all(line.startswith("    ") for line in exc_lines)
        assert all(line.startswith("    ") for line in stack_lines)


@pytest.mark.parametrize("style", ["%"])
def test_detailed_formatter_style_variants(
    log_record_factory: Callable[..., logging.LogRecord], style: str
) -> None:
    fmt = DetailedFormatter(style=style)
    record = log_record_factory(msg="style test")
    output = fmt.format(record)
    assert "style test" in output


def test_detailed_formatter_repr_and_str(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    record = log_record_factory(msg="repr test")
    output = fmt.format(record)
    assert isinstance(output, str)


def test_detailed_formatter_empty_message(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    record = log_record_factory(msg="")
    output = fmt.format(record)
    assert isinstance(output, str)
    assert output


def test_detailed_formatter_metadata_len_minus_one(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    custom_fmt = "%(asctime)s [%(levelname)s] [%(name)s]\n%(message)s"
    fmt = DetailedFormatter(fmt=custom_fmt)
    msg = "should not be found\nsecond line"
    record = log_record_factory(msg=msg)
    output = fmt.format(record)
    assert "should not be found" in output
    assert "second line" in output
    lines = output.splitlines()
    assert "should not be found" not in lines[0]
    assert lines[1].lstrip() == "should not be found"
    assert lines[1].startswith(" ")
    assert lines[2].lstrip() == "second line" and lines[2].startswith(" ")
    assert isinstance(output, str)
    assert output


def test_detailed_formatter_exc_info_sets_exc_text(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    try:
        raise KeyError("trigger exc_info path")
    except KeyError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="exception path", exc_info=exc_info)
        record.exc_text = None
        output = fmt.format(record)
        assert "KeyError: 'trigger exc_info path'" in output


def test_detailed_formatter_exc_info_sets_exc_text_branch(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = DetailedFormatter()
    try:
        raise KeyError("trigger exc_info path")
    except KeyError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="exception path", exc_info=exc_info)
        if hasattr(record, "exc_text"):
            delattr(record, "exc_text")
        output = fmt.format(record)
        assert "KeyError: 'trigger exc_info path'" in output


def test_detailed_formatter_format_exception_text_direct(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    """Test that directly calls _format_exception_text to ensure line 72 is covered."""
    fmt = DetailedFormatter()
    try:
        raise ValueError("direct test")
    except ValueError:
        exc_info = sys.exc_info()
        record = log_record_factory(msg="direct test", exc_info=exc_info)

        # Ensure exc_text is not set
        if hasattr(record, "exc_text"):
            delattr(record, "exc_text")

        # Call _format_exception_text directly
        formatted = ""
        formatted = fmt._format_exception_text(formatted, record)

        # Verify exc_text was set by the method
        assert hasattr(record, "exc_text")
        assert record.exc_text is not None
        assert "ValueError: direct test" in record.exc_text
        assert "ValueError: direct test" in formatted
