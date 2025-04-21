import logging
import sys
from typing import IO, Optional


class ConsoleHandler(logging.StreamHandler[IO[str]]):
    """
    A custom logging handler that writes log records to a stream (like stderr).

    This handler is essentially a wrapper around `logging.StreamHandler`
    but provides a convenient way to configure console logging within
    the apiconfig library and allows for future customization.
    """

    def __init__(self, stream: Optional[IO[str]] = None) -> None:
        """
        Initialize the handler.

        Parameters
        ----------
        stream : Optional[IO[str]], optional
            The stream to write log records to. Defaults to `sys.stderr`.
        """
        super().__init__(stream or sys.stderr)


class RedactingStreamHandler(logging.StreamHandler[IO[str]]):
    """
    A basic stream handler, placeholder for potential redaction logic.

    Placeholder - inherits methods from logging.StreamHandler.
    """

    # Placeholder implementation - inherits default behavior
