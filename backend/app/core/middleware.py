from __future__ import annotations

import logging
import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        start = time.perf_counter()
        client_host = request.client.host if request.client else "-"
        ua = request.headers.get("user-agent", "-")
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            status = response.status_code
            return response
        finally:
            duration_ms = (time.perf_counter() - start) * 1000.0
            logger.info(
                "http_request",
                extra={
                    "method": method,
                    "path": path,
                    "status": locals().get("status", 500),
                    "duration_ms": round(duration_ms, 2),
                    "client": client_host,
                    "user_agent": ua[:200],
                },
            )
