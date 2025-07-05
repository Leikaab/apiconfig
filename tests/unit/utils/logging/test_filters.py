import logging
from typing import Any, Generator  # pyright: ignore[reportShadowedImports]

import pytest

from apiconfig.utils.logging.filters import (
    ContextFilter,
    clear_log_context,
    set_log_context,
)


@pytest.fixture(autouse=True)
def clear_context() -> Generator[None, None, None]:
    """Ensure log context is clear before and after each test."""
    clear_log_context()
    yield
    clear_log_context()


def test_set_log_context_sets_value() -> None:
    set_log_context("user_id", 123)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )
    f = ContextFilter()
    f.filter(record)
    assert getattr(record, "user_id", None) == 123


def test_clear_log_context_removes_all_keys() -> None:
    set_log_context("foo", "bar")
    set_log_context("baz", 42)
    clear_log_context()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )
    f = ContextFilter()
    f.filter(record)
    # After clearing, none of the context keys should be present
    assert not hasattr(record, "foo")
    assert not hasattr(record, "baz")


@pytest.mark.parametrize(
    "context",
    [
        {},
        {"user": "alice", "request_id": "abc123"},
    ],
)
def test_context_filter_filter_adds_context_to_record(context: dict[str, Any]) -> None:
    clear_log_context()
    for k, v in context.items():
        set_log_context(k, v)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )
    f = ContextFilter()
    result = f.filter(record)
    assert result is True
    for k, v in context.items():
        assert getattr(record, k) == v


def test_context_filter_filter_no_context_does_not_fail() -> None:
    clear_log_context()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )
    f = ContextFilter()
    result = f.filter(record)
    assert result is True
    # No extra attributes should be set
    assert not hasattr(record, "foo")
    assert not hasattr(record, "user_id")
