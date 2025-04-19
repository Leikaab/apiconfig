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

    def __init__(self, stream: Optional[IO[str]] = ...) -> None:
        """
        Initialize the handler.

        Args:
            stream: The stream to write log records to. Defaults to `sys.stderr`.
        """
        ...
