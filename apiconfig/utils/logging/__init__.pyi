"""Type stubs for apiconfig.utils.logging."""

from .formatters import DetailedFormatter
from .handlers import ConsoleHandler

__all__: list[str] = ["DetailedFormatter", "ConsoleHandler"]
