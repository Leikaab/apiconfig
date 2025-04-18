import logging
import sys
from typing import IO, Optional


class ConsoleHandler(logging.StreamHandler):
    """
    A logging handler that writes records to the console (stderr by default).

    This handler is essentially a wrapper around `logging.StreamHandler`
    configured for console output, providing a convenient way to ensure
    consistent console logging within the library and allowing for future
    customizations specific to apiconfig's console output needs.
    """

    def __init__(self, stream: Optional[IO[str]] = None) -> None:
        """
        Initializes the handler to send records to a stream.

        Args:
            stream: The stream to write log records to. Defaults to `sys.stderr`.
        """
        # Default to stderr if no stream is provided
        if stream is None:
            stream = sys.stderr
        super().__init__(stream)
