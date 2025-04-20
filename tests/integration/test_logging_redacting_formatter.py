import io
import logging
import re
from typing import Any, Generator, Protocol

import pytest

from apiconfig.utils.logging.formatters import RedactingFormatter


@pytest.fixture
def log_stream() -> Generator[io.StringIO, None, None]:
    stream = io.StringIO()
    yield stream
    stream.close()


def get_logger_with_formatter(stream: io.StringIO, **fmt_kwargs: Any) -> logging.Logger:
    logger = logging.getLogger("integration.redact")
    logger.handlers.clear()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(RedactingFormatter(**fmt_kwargs))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def test_redacting_formatter_integration_json(log_stream: io.StringIO) -> None:
    logger = get_logger_with_formatter(log_stream)
    logger.info('{"token": "abc123", "data": "ok"}')
    output = log_stream.getvalue()
    assert "[REDACTED]" in output
    assert "abc123" not in output


def test_redacting_formatter_integration_dict(log_stream: io.StringIO) -> None:
    logger = get_logger_with_formatter(log_stream)
    logger.info({"password": "p@ssw0rd", "foo": "bar"})
    output = log_stream.getvalue()
    assert "[REDACTED]" in output
    assert "p@ssw0rd" not in output


def test_redacting_formatter_integration_form(log_stream: io.StringIO) -> None:
    logger = get_logger_with_formatter(log_stream)
    logger.info(
        "secret=shh123&foo=bar",
        extra={"content_type": "application/x-www-form-urlencoded"},
    )
    output = log_stream.getvalue()
    # Accept both [REDACTED] and %5BREDACTED%5D for form-encoded output
    assert "[REDACTED]" in output or "%5BREDACTED%5D" in output
    assert "shh123" not in output


def test_redacting_formatter_integration_headers(log_stream: io.StringIO) -> None:
    logger = get_logger_with_formatter(log_stream)
    logger.info(
        "header test",
        extra={
            "headers": {
                "Authorization": "Bearer abc",
                "X-Api-Key": "xyz",
                "X-Other": "ok",
            }
        },
    )
    # The headers dict is not in the message, but we can check the record
    # For integration, we check that the record's headers are redacted
    # (This is a limitation of logging, but we can at least check the handler's formatter)
    # So we check that the handler's formatter redacts headers
    record = logging.LogRecord(
        name="integration.redact",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="header test",
        args=(),
        exc_info=None,
        func=None,
        sinfo=None,
    )
    from typing import cast

    setattr(
        record,
        "headers",
        {"Authorization": "Bearer abc", "X-Api-Key": "xyz", "X-Other": "ok"},
    )

    class TypedLogRecord(Protocol):
        headers: dict[str, str]

    handler = logging.StreamHandler(io.StringIO())
    handler.setFormatter(RedactingFormatter())
    handler.format(record)
    # Use cast only for attribute access
    headers = cast(TypedLogRecord, record).headers
    assert headers["Authorization"] == "[REDACTED]"
    assert headers["X-Api-Key"] == "[REDACTED]"
    assert headers["X-Other"] == "ok"


def test_redacting_formatter_integration_plain_string(log_stream: io.StringIO) -> None:
    secret_pattern = re.compile(r"secret_[a-z0-9]+", re.IGNORECASE)
    logger = get_logger_with_formatter(
        log_stream, body_sensitive_value_pattern=secret_pattern
    )
    logger.info("this is a secret_abc123 and should be redacted")
    output = log_stream.getvalue()
    assert "[REDACTED]" in output
    assert "secret_abc123" not in output


def test_redacting_formatter_integration_binary(log_stream: io.StringIO) -> None:
    logger = get_logger_with_formatter(log_stream)
    logger.info(b"\x00\x01\x02\x03", extra={"content_type": "application/octet-stream"})
    output = log_stream.getvalue()
    assert "[REDACTED BODY]" in output


def test_redacting_formatter_integration_empty(log_stream: io.StringIO) -> None:
    logger = get_logger_with_formatter(log_stream)
    logger.info("")
    output = log_stream.getvalue()
    assert "[REDACTED]" in output
