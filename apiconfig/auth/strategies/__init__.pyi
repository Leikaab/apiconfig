"""Type stubs for authentication strategies."""


from .basic import BasicAuth
from .bearer import BearerAuth

__all__ = ["BasicAuth", "BearerAuth"]
