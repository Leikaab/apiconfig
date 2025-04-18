# -*- coding: utf-8 -*-
"""
apiconfig: A library for flexible API configuration and authentication.

This library provides components for managing API client configurations
(like base URLs, timeouts, retries) and handling various authentication
strategies (Basic, Bearer, API Key, etc.).
"""

__version__ = "0.1.0"  # Placeholder version

# Import key components to make them available at the package level (optional)
# Example:
# from .config import ClientConfig
# from .auth import AuthStrategy, BasicAuth, BearerAuth

# Configure logging (optional, can be done here or by the application)
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
