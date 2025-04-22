# -*- coding: utf-8 -*-
"""Logging filters, including context injection."""

import logging
import threading
from typing import Any

_log_context = threading.local()


class ContextFilter(logging.Filter):
    """Inject context variables from thread-local storage into log records.

    Usage
    -----
    Add this filter to a logger's handler. Then use `set_log_context`
    to add context variables within your code (e.g., request ID, user ID).
    These variables will be automatically added to log records processed
    by handlers using this filter. Remember to clear the context when appropriate
    (e.g., at the end of a request) using `clear_log_context`.

    Example Formatter Usage
    -----------------------
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
    )
    # Assuming 'request_id' was set using set_log_context('request_id', ...)
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Add context variables from thread-local storage to the log record.

        Args
        ----
        record
            The log record to be processed.

        Returns
        -------
        bool
            True to indicate the record should be processed.
        """
        context_data = getattr(_log_context, "__dict__", {})
        for key, value in context_data.items():
            setattr(record, key, value)
        return True


def set_log_context(key: str, value: Any) -> None:
    """Set a key-value pair in the thread-local context for logging.

    Args
    ----
    key
        The context key (will become an attribute on the log record).
    value
        The context value.
    """
    setattr(_log_context, key, value)


def clear_log_context() -> None:
    """Clear all context variables from the thread-local storage."""
    if hasattr(_log_context, "__dict__"):
        _log_context.__dict__.clear()
