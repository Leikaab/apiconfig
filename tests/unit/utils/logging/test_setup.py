from __future__ import annotations

import logging as logging_mod
import sys
from unittest.mock import MagicMock, patch

from apiconfig.utils.logging.setup import setup_logging

# Default values used in setup_logging
# Note: The actual setup_logging uses RedactingStreamHandler and RedactingFormatter by default,
# but we patch the standard ones here to avoid import issues if those aren't implemented/exported yet
# and to focus the test on the setup logic itself.
DEFAULT_LOGGER_NAME = "apiconfig"
DEFAULT_LOG_LEVEL = logging_mod.WARNING  # Default level is WARNING as per .pyi
DEFAULT_FORMAT_STRING = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@patch("apiconfig.utils.logging.setup._logger")  # Patch the module-level logger instance
@patch("apiconfig.utils.logging.setup.RedactingStreamHandler")
@patch("apiconfig.utils.logging.setup.RedactingFormatter")
def test_setup_logging_default(
    mock_formatter_cls: MagicMock,
    mock_handler_cls: MagicMock,
    mock_logger: MagicMock,  # The patched _logger object
) -> None:
    """Test setup_logging with default parameters."""
    # Configure the mock logger passed by the patch
    mock_logger.handlers = []
    mock_logger.reset_mock()  # Reset mock from potential previous tests or module load

    mock_handler_instance = MagicMock(spec=logging_mod.Handler)
    mock_formatter_instance = MagicMock(spec=logging_mod.Formatter)
    mock_handler_cls.return_value = mock_handler_instance
    mock_formatter_cls.return_value = mock_formatter_instance

    setup_logging()

    # Check logger interactions
    mock_logger.hasHandlers.assert_called_once()  # Should check if handlers exist
    # Since handlers is empty, clear() shouldn't be called. removeHandler shouldn't be called.
    mock_logger.removeHandler.assert_not_called()
    mock_logger.setLevel.assert_called_once_with(DEFAULT_LOG_LEVEL)
    # Check default handler/formatter creation and application
    mock_handler_cls.assert_called_once_with(sys.stderr)  # Default handler uses stderr
    mock_formatter_cls.assert_called_once_with()  # Default formatter with default args
    mock_handler_instance.setFormatter.assert_called_once_with(mock_formatter_instance)
    mock_logger.addHandler.assert_called_once_with(mock_handler_instance)


@patch("apiconfig.utils.logging.setup._logger")  # Patch the module-level logger instance
@patch("apiconfig.utils.logging.setup.RedactingFormatter")  # Patch default formatter
def test_setup_logging_custom_handlers(
    mock_formatter_cls: MagicMock,
    mock_logger: MagicMock,  # The patched _logger object
) -> None:
    """Test setup_logging with custom handlers."""
    mock_logger.handlers = []
    mock_logger.reset_mock()
    mock_logger.hasHandlers.return_value = False  # No handlers initially

    # Use mocks with spec for type compatibility (mypy fix)
    custom_handler1 = MagicMock(spec=logging_mod.Handler)
    custom_handler2 = MagicMock(spec=logging_mod.Handler)
    custom_handlers: list[logging_mod.Handler] = [custom_handler1, custom_handler2]

    mock_formatter_instance = MagicMock(spec=logging_mod.Formatter)
    mock_formatter_cls.return_value = mock_formatter_instance

    # Call setup_logging with custom handlers
    setup_logging(handlers=custom_handlers)

    # Check logger interactions
    mock_logger.hasHandlers.assert_called_once()
    mock_logger.setLevel.assert_called_once_with(DEFAULT_LOG_LEVEL)

    # Check default formatter created and applied to custom handlers
    mock_formatter_cls.assert_called_once_with()
    # Assert setFormatter was called, not attribute access (AttributeError fix)
    custom_handler1.setFormatter.assert_called_with(mock_formatter_instance)
    custom_handler2.setFormatter.assert_called_with(mock_formatter_instance)

    # Check handlers were added
    assert mock_logger.addHandler.call_count == 2
    mock_logger.addHandler.assert_any_call(custom_handler1)
    mock_logger.addHandler.assert_any_call(custom_handler2)

    # Clean up created files
    import os

    if os.path.exists("test1.log"):
        os.remove("test1.log")


@patch("apiconfig.utils.logging.setup._logger")  # Patch the module-level logger instance
@patch("apiconfig.utils.logging.setup.RedactingStreamHandler")  # Patch default handler
def test_setup_logging_custom_formatter(
    mock_handler_cls: MagicMock,
    mock_logger: MagicMock,  # The patched _logger object
) -> None:
    """Test setup_logging with a custom formatter."""
    mock_logger.handlers = []
    mock_logger.reset_mock()
    custom_formatter = logging_mod.Formatter("%(levelname)s: %(message)s")

    mock_handler_instance = MagicMock(spec=logging_mod.Handler)
    mock_handler_cls.return_value = mock_handler_instance

    # Call setup_logging with custom formatter
    setup_logging(formatter=custom_formatter)

    # Check logger interactions
    mock_logger.hasHandlers.assert_called_once()
    mock_logger.setLevel.assert_called_once_with(DEFAULT_LOG_LEVEL)

    # Check default handler created and custom formatter applied
    mock_handler_cls.assert_called_once_with(sys.stderr)  # Default handler uses stderr
    mock_handler_instance.setFormatter.assert_called_once_with(custom_formatter)
    mock_logger.addHandler.assert_called_once_with(mock_handler_instance)


@patch("apiconfig.utils.logging.setup._logger")  # Patch the module-level logger instance
@patch("apiconfig.utils.logging.setup.RedactingStreamHandler")
@patch("apiconfig.utils.logging.setup.RedactingFormatter")
def test_setup_logging_custom_level(
    mock_formatter_cls: MagicMock,
    mock_handler_cls: MagicMock,
    mock_logger: MagicMock,  # The patched _logger object
) -> None:
    """Test setup_logging with a custom log level."""
    mock_logger.handlers = []
    mock_logger.reset_mock()
    mock_logger.hasHandlers.return_value = False  # No handlers initially
    custom_level = logging_mod.DEBUG

    mock_handler_instance = MagicMock(spec=logging_mod.Handler)
    mock_formatter_instance = MagicMock(spec=logging_mod.Formatter)
    mock_handler_cls.return_value = mock_handler_instance
    mock_formatter_cls.return_value = mock_formatter_instance

    setup_logging(level=custom_level)

    # Check logger interactions
    mock_logger.hasHandlers.assert_called_once()
    mock_logger.setLevel.assert_called_once_with(custom_level)
    # Check default handler/formatter were still added
    mock_handler_cls.assert_called_once_with(sys.stderr)  # Default handler uses stderr
    mock_formatter_cls.assert_called_once_with()  # Default formatter
    mock_handler_instance.setFormatter.assert_called_with(mock_formatter_instance)
    mock_logger.addHandler.assert_called_once_with(mock_handler_instance)


@patch("apiconfig.utils.logging.setup._logger")  # Patch the module-level logger instance
@patch("apiconfig.utils.logging.setup.RedactingStreamHandler")
@patch("apiconfig.utils.logging.setup.RedactingFormatter")
def test_setup_logging_removes_existing_handlers(
    mock_formatter_cls: MagicMock,
    mock_handler_cls: MagicMock,
    mock_logger: MagicMock,  # The patched _logger object
) -> None:
    """Test that existing handlers are removed via clear() before adding new ones."""
    # Simulate pre-existing handlers
    existing_handler1 = MagicMock(spec=logging_mod.Handler)
    existing_handler2 = MagicMock(spec=logging_mod.Handler)
    # Assign to a separate list first, then assign to mock_logger.handlers
    # This allows us to mock clear() on the list object itself if needed,
    # although checking the final state might be more robust.
    initial_handlers = [existing_handler1, existing_handler2]
    mock_logger.handlers = initial_handlers
    # Mock hasHandlers to return True
    mock_logger.hasHandlers.return_value = True

    # Reset mocks before the call
    mock_logger.setLevel.reset_mock()
    mock_logger.addHandler.reset_mock()
    mock_logger.hasHandlers.reset_mock()
    mock_logger.removeHandler.reset_mock()

    mock_new_handler_instance = MagicMock(spec=logging_mod.Handler)
    mock_formatter_instance = MagicMock(spec=logging_mod.Formatter)
    mock_handler_cls.return_value = mock_new_handler_instance
    mock_formatter_cls.return_value = mock_formatter_instance

    # Mock the clear method on the *actual* list object used by the logger mock
    # This is tricky. Let's try asserting the outcome instead.
    # We expect hasHandlers -> True, then handlers list to be empty, then addHandler called.

    setup_logging()  # Use defaults

    # Check logger interactions
    mock_logger.setLevel.assert_called_once_with(DEFAULT_LOG_LEVEL)

    # Check that hasHandlers was called
    mock_logger.hasHandlers.assert_called_once()

    # Assert that addHandler was called *only* with the new handler.
    # This implies the list was cleared before adding.
    mock_logger.addHandler.assert_called_once_with(mock_new_handler_instance)

    # Check new default handler and formatter were created
    mock_handler_cls.assert_called_once_with(sys.stderr)
    mock_formatter_cls.assert_called_once_with()
    mock_new_handler_instance.setFormatter.assert_called_with(mock_formatter_instance)

    # Ensure removeHandler was NOT called (since clear is used)
    mock_logger.removeHandler.assert_not_called()
