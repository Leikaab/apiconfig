# -*- coding: utf-8 -*-
"""Base authentication classes."""

from abc import ABC, abstractmethod
from typing import Dict


class AuthStrategy(ABC):
    """Base class for authentication strategies."""

    @abstractmethod
    def prepare_request_headers(self) -> Dict[str, str]:
        """Prepare authentication headers for an HTTP request."""
        pass  # pragma: no cover

    @abstractmethod
    def prepare_request_params(self) -> Dict[str, str]:
        """Prepare authentication parameters for an HTTP request."""
        pass  # pragma: no cover
