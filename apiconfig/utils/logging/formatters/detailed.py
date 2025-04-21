# -*- coding: utf-8 -*-
"""Detailed logging formatter."""

import logging
import textwrap
import types
from typing import Any, Literal, Mapping, Optional


class DetailedFormatter(logging.Formatter):
    """
    A logging formatter that provides detailed, potentially multi-line output.

    Includes timestamp, level name, logger name, message, filename, and line number.
    Handles multi-line messages, exception information, and stack information
    with appropriate indentation.
    """

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        *,
        defaults: Optional[Mapping[str, Any]] = None,
    ) -> None:
        # Default format string
        default_fmt = "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s" "\n    (%(filename)s:%(lineno)d)"
        super().__init__(
            fmt=fmt or default_fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
            defaults=defaults,
        )

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text.

        Handles multi-line messages, exception text, and stack information.

        Args
        ----
        record
            The log record to format.

        Returns
        -------
        str
            The formatted log record.
        """
        if not hasattr(record, "exc_text"):
            record.exc_text = None
        formatted = super().format(record)
        formatted = self._format_multiline_message(formatted, record)
        formatted = self._format_exception_text(formatted, record)
        formatted = self._format_stack_info(formatted, record)
        return formatted

    def _format_multiline_message(self, formatted: str, record: logging.LogRecord) -> str:
        lines = formatted.split("\n")
        if len(lines) <= 1:
            return formatted
        first_line = lines[0]
        message_lines = record.getMessage().split("\n")
        metadata_len = first_line.find(message_lines[0])
        if metadata_len == -1:
            metadata_len = len(first_line) - len(message_lines[0])
        if len(message_lines) > 1:
            indented_message = "\n".join([message_lines[0]] + [textwrap.indent(line, " " * (metadata_len)) for line in message_lines[1:]])
            lines[0] = first_line.replace(message_lines[0], indented_message.split("\n", 1)[0])
        other_lines = [lines[0]] + [textwrap.indent(line, "    ") for line in lines[1:]]
        if len(message_lines) > 1:
            other_lines.extend(textwrap.indent(line, " " * (metadata_len)) for line in message_lines[1:])
        return "\n".join(other_lines)

    def formatException(
        self,
        ei: tuple[type[BaseException], BaseException, types.TracebackType | None] | tuple[None, None, None],
    ) -> str:
        """Format the specified exception information as a string.

        This implementation delegates to the base class.

        Args
        ----
        ei
            Exception info tuple as returned by sys.exc_info().

        Returns
        -------
        str
            The formatted exception string.
        """
        return super().formatException(ei)

    def formatStack(self, stack_info: str) -> str:
        """Format the specified stack information as a string.

        This implementation delegates to the base class.

        Args
        ----
        stack_info
            Stack information string.

        Returns
        -------
        str
            The formatted stack string.
        """
        return super().formatStack(stack_info)

    def _format_exception_text(self, formatted: str, record: logging.LogRecord) -> str:
        if record.exc_info and not getattr(record, "exc_text", None):
            record.exc_text = self.formatException(record.exc_info)
        if getattr(record, "exc_text", None):
            exc_text = textwrap.indent(record.exc_text if record.exc_text is not None else "", "    ")
            if formatted[-1:] != "\n":
                formatted += "\n"
            formatted += exc_text
        return formatted

    def _format_stack_info(self, formatted: str, record: logging.LogRecord) -> str:
        if record.stack_info:
            stack_info = textwrap.indent(self.formatStack(record.stack_info), "    ")
            if formatted[-1:] != "\n":
                formatted += "\n"
            formatted += stack_info
        return formatted
