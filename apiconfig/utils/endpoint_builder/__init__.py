"""
Endpoint builder module for constructing API endpoint paths.

This module provides utilities for building API endpoint paths with support
for nested resources, validation, and path manipulation.

The main class is EndpointBuilder, which orchestrates the endpoint construction
process. Additional utility functions are available for specific tasks like
path validation and segment manipulation.
"""

from .builder import EndpointBuilder
from .path_utils import join_path_segments
from .segments import build_resource_segments
from .validators import validate_path_segments

__all__ = [
    "EndpointBuilder",
    "validate_path_segments",
    "join_path_segments",
    "build_resource_segments",
]
