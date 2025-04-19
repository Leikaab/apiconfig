import logging
import textwrap
from typing import Literal  # Add Literal import


class DetailedFormatter(logging.Formatter):
    """A logging formatter that provides detailed, potentially multi-line output."""

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",  # Correct the type hint
        validate: bool = True,
        *,
        defaults: dict | None = None,
    ) -> None:
        # Default format string
        default_fmt = (
            "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s"
            "\n    (%(filename)s:%(lineno)d)"
        )
        super().__init__(
            fmt=fmt or default_fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
            defaults=defaults,
        )

    def format(self, record: logging.LogRecord) -> str:
        # Format the first line using the base class
        formatted = super().format(record)

        # Handle potential multi-line messages
        lines = formatted.split("\n")
        if len(lines) > 1:
            first_line = lines[0]
            # Indent subsequent lines of the message itself if they exist
            # The base formatter might already handle some indentation,
            # but we ensure consistent indentation for message lines beyond the first.
            # We assume the core message starts after the initial metadata.
            metadata_len = first_line.find(record.getMessage().split("\n", 1)[0])
            if metadata_len == -1:
                metadata_len = len(first_line) - len(
                    record.getMessage().split("\n", 1)[0]
                )

            # Indent message lines
            message_lines = record.getMessage().split("\n")
            if len(message_lines) > 1:
                indented_message = "\n".join(
                    [message_lines[0]]
                    + [
                        textwrap.indent(line, " " * (metadata_len))
                        for line in message_lines[1:]
                    ]
                )
                # Reconstruct the first line with potentially modified message part
                lines[0] = first_line.replace(
                    record.getMessage().split("\n", 1)[0],
                    indented_message.split("\n", 1)[0],
                )

            # Indent any extra lines added by the formatter (like file/line info)
            # and the rest of the message lines
            other_lines = [lines[0]] + [
                textwrap.indent(line, "    ") for line in lines[1:]
            ]

            # Combine message lines (already indented) with other indented lines
            if len(message_lines) > 1:
                other_lines.extend(
                    textwrap.indent(line, " " * (metadata_len))
                    for line in message_lines[1:]
                )

            formatted = "\n".join(other_lines)

        # Handle exception info if present
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # Indent exception text
            exc_text = textwrap.indent(record.exc_text, "    ")
            if formatted[-1:] != "\n":
                formatted += "\n"
            formatted += exc_text

        # Handle stack info if present
        if record.stack_info:
            # Indent stack info
            stack_info = textwrap.indent(self.formatStack(record.stack_info), "    ")
            if formatted[-1:] != "\n":
                formatted += "\n"
            formatted += stack_info

        return formatted
