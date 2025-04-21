from __future__ import annotations

import io
import sys

from apiconfig.utils.logging.handlers import ConsoleHandler


def test_console_handler_defaults_to_stderr() -> None:
    handler = ConsoleHandler()
    assert handler.stream is sys.stderr


def test_console_handler_with_custom_stream() -> None:
    stream = io.StringIO()
    handler = ConsoleHandler(stream=stream)
    assert handler.stream is stream
