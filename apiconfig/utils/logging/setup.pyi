import logging
from typing import List, Optional, Union

_logger: logging.Logger

def setup_logging(
    level: Union[int, str] = logging.WARNING,
    handlers: Optional[List[logging.Handler]] = None,
    formatter: Optional[logging.Formatter] = None,
) -> None:
    """
    Configures logging for the apiconfig library.

    Sets the logging level for the root 'apiconfig' logger and adds
    specified handlers. If no handlers are provided, a default
    RedactingStreamHandler writing to stderr is added. A default
    RedactingFormatter is applied to all handlers unless a specific
    formatter is provided.

    Note: This function removes any previously configured handlers
    on the 'apiconfig' logger before adding the new ones.

    Args:
        level: The minimum logging level for the 'apiconfig' logger.
            Can be an integer (e.g., logging.DEBUG) or a string name
            (e.g., "DEBUG", "INFO", "WARNING"). Defaults to logging.WARNING.
        handlers: An optional list of logging handler instances to add
            to the 'apiconfig' logger. If None or empty, a default
            RedactingStreamHandler(sys.stderr) will be added.
        formatter: An optional logging formatter instance to apply to the handlers.
            If None, a default RedactingFormatter will be used.

    Examples:
        >>> import logging
        >>> from apiconfig.utils.logging import setup_logging

        # Apply default logging (WARNING level, RedactingStreamHandler to stderr)
        >>> setup_logging()
        >>> logging.getLogger("apiconfig").warning("This is a warning.")

        # Set level to DEBUG and add a custom file handler
        >>> import sys
        >>> from apiconfig.utils.logging.handlers import RedactingStreamHandler
        >>> file_handler = logging.FileHandler("apiconfig.log")
        >>> custom_handlers = [RedactingStreamHandler(sys.stdout), file_handler]
        >>> setup_logging(level=logging.DEBUG, handlers=custom_handlers)
        >>> logging.getLogger("apiconfig").debug("This is a debug message.")
    """
    ...
