from typing import Any, List, Mapping, Pattern, Tuple

from werkzeug.wrappers import Request, Response

class RequestHandler:

    def respond_with_json(
        self,
        response_json: Any,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
        content_type: str = "application/json",
    ) -> None: ...

    def respond_with_response(self, response: Response, **kwargs: Any) -> None: ...

class HTTPServer:
    log: List[Tuple[Request, Response]]
    def expect_request(
        self,
        uri: str | Pattern[str],
        method: str = "GET",
        *,
        ordered: bool = ...,
        **kwargs: Any,
    ) -> RequestHandler: ...
    def url_for(self, suffix: str) -> str: ...

