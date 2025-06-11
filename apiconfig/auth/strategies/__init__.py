"""Authentication strategies for apiconfig."""

from .api_key import ApiKeyAuth
from .basic import BasicAuth
from .bearer import BearerAuth
from .custom import CustomAuth

__all__: list[str] = ["ApiKeyAuth", "BasicAuth", "BearerAuth", "CustomAuth"]
