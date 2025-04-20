import logging
from typing import Any, Callable

import pytest

from apiconfig.utils.logging.formatters import RedactingFormatter


class TypedLogRecord(logging.LogRecord):
    headers: dict[str, str]


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
        expected in output
        or expected.replace("%5BREDACTED%5D", "[REDACTED]") in output
        or expected.replace("[REDACTED]", "%5BREDACTED%5D") in output
    )


def test_redacting_formatter_headers_redaction(
    log_record_factory: Callable[..., logging.LogRecord],
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="headers test")
    from typing import cast

    setattr(
        record,
        "headers",
        {"Authorization": "Bearer abc", "X-Api-Key": "xyz", "X-Other": "ok"},
    )
    record = cast(TypedLogRecord, record)
    fmt.format(record)
    assert (
        '"Authorization": "[REDACTED]"' in str(record.headers)
        or "'Authorization': '[REDACTED]'" in str(record.headers)
        or "[REDACTED]" in str(record.headers)
    )
    assert "[REDACTED]" in str(record.headers)
    assert "ok" in str(record.headers)


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
    monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg="headers test")
    from typing import cast
    setattr(record, "headers", {"Authorization": "Bearer abc"})
    record = cast(TypedLogRecord, record)

    def bad_redact_headers(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr(
        "apiconfig.utils.logging.formatters.redact_headers", bad_redact_headers
    )
    fmt._redact_headers_func = bad_redact_headers
    fmt.format(record)
    assert record.headers == {"Authorization": "Bearer abc"}


def test_redacting_formatter_redact_structured_exception(
    monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"foo": "bar"})

    def bad_redact_body(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr(
        "apiconfig.utils.logging.formatters.redact_body", bad_redact_body
    )
    fmt._redact_body = bad_redact_body
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
    monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg='{"token": "abc"}')

    def bad_redact_body(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr(
        "apiconfig.utils.logging.formatters.redact_body", bad_redact_body
    )
    fmt._redact_body = bad_redact_body
    output = fmt.format(record)
    assert '{"token": "abc"}' in output


def test_redacting_formatter_structured_dict_exception(
    monkeypatch: Any, log_record_factory: Callable[..., logging.LogRecord]
) -> None:
    fmt = RedactingFormatter()
    record = log_record_factory(msg={"token": "abc"})

    def bad_redact_body(*a: object, **kw: object) -> None:
        raise RuntimeError("fail")
    monkeypatch.setattr(
        "apiconfig.utils.logging.formatters.redact_body", bad_redact_body
    )
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
