from typing import Any, List, Tuple
from werkzeug.wrappers import Request, Response

class RequestHandler:
    def respond_with_response(self, response: Response, **kwargs: Any) -> None: ...

class HTTPServer:
    log: List[Tuple[Request, Response]]
    def expect_request(self, uri: str, method: str = "GET", *, ordered: bool = ..., **kwargs: Any) -> RequestHandler: ...
