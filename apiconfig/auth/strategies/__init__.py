"""Authentication strategies for apiconfig."""


from .basic import BasicAuth
from .bearer import BearerAuth

__all__ = ["BasicAuth", "BearerAuth"]
