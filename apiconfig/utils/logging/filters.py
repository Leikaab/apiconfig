import logging
import threading
from typing import Any

_log_context = threading.local()


class ContextFilter(logging.Filter):
    """
    A logging filter that injects context variables from thread-local storage
    into log records.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Adds context variables from thread-local storage to the log record.

        Args:
            record: The log record to be processed.

        Returns:
            True to indicate the record should be processed.
        """
        context_data = getattr(_log_context, "__dict__", {})
        for key, value in context_data.items():
            setattr(record, key, value)
        return True


def set_log_context(key: str, value: Any) -> None:
    """
    Sets a key-value pair in the thread-local context for logging.

    Args:
        key: The context key (will become an attribute on the log record).
        value: The context value.
    """
    setattr(_log_context, key, value)


def clear_log_context() -> None:
    """Clears all context variables from the thread-local storage."""
    if hasattr(_log_context, "__dict__"):
        _log_context.__dict__.clear()
