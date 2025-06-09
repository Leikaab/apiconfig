from typing import Any, Pattern, Mapping
from werkzeug.wrappers import Request, Response

class RequestHandler:
    def respond_with_response(self, response: Response, **kwargs: Any) -> None: ...

class HTTPServer:
    def expect_request(self, *args: Any, ordered: bool = ..., **kwargs: Any) -> RequestHandler: ...
