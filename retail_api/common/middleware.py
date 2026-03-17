import json
import logging
import time
import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from retail_api.common.metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION

logger = logging.getLogger(__name__)


def _structured_log(level: str, message: str, request_id: str, **extra: object) -> None:
    record = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "level": level,
        "message": message,
        "request_id": request_id,
        **extra,
    }
    print(json.dumps(record), flush=True)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex
        request.state.request_id = request_id
        _structured_log("INFO", f"{request.method} {request.url.path}", request_id)
        path = request.scope.get("path", "")
        method = request.method
        start = time.perf_counter()
        response = await call_next(request)
        HTTP_REQUESTS_TOTAL.labels(method=method, path=path).inc()
        HTTP_REQUEST_DURATION.labels(method=method, path=path).observe(
            time.perf_counter() - start
        )
        response.headers["X-Request-Id"] = request_id
        return response
