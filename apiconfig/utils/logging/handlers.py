import logging
import sys
from typing import IO, Optional


class ConsoleHandler(logging.StreamHandler):
    def __init__(self, stream: Optional[IO[str]] = None) -> None:
        super().__init__(stream or sys.stderr)
