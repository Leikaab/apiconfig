import logging
import types
from typing import Any, Mapping

_FormatStyle = logging._FormatStyle

class DetailedFormatter(logging.Formatter):
    """
    A logging formatter that provides detailed, potentially multi-line output.

    Includes timestamp, level name, logger name, message, filename, and line number.
    Handles multi-line messages, exception information, and stack information
    with appropriate indentation.
    """

    def __init__(
        self,
        fmt: str | None = ...,
        datefmt: str | None = ...,
        style: _FormatStyle = ...,
        validate: bool = ...,
        *,
        defaults: Mapping[str, Any] | None = ...,
    ) -> None: ...
    def format(self, record: logging.LogRecord) -> str: ...
    def formatException(
        self,
        ei: (
            tuple[type[BaseException], BaseException, types.TracebackType | None]
            | tuple[None, None, None]
        ),
    ) -> str: ...
    def formatStack(self, stack_info: str) -> str: ...
