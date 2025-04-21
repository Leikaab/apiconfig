import logging
from typing import Any

class ContextFilter(logging.Filter):
    """
    A logging filter that injects context variables from thread-local storage
    into log records.

    Usage:
        Add this filter to a logger's handler. Then use `set_log_context`
        to add context variables within your code (e.g., request ID, user ID).
        These variables will be automatically added to log records processed
        by handlers using this filter. Remember to clear the context when appropriate
        (e.g., at the end of a request) using `clear_log_context`.

    Example Formatter Usage:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
        )
        # Assuming 'request_id' was set using set_log_context('request_id', ...)
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Adds context variables from thread-local storage to the log record.

        Args:
            record: The log record to be processed.

        Returns:
            True to indicate the record should be processed.
        """
        ...

def set_log_context(key: str, value: Any) -> None:
    """
    Sets a key-value pair in the thread-local context for logging.

    Args:
        key: The context key (will become an attribute on the log record).
        value: The context value.
    """
    ...

def clear_log_context() -> None:
    """Clears all context variables from the thread-local storage."""
    ...
