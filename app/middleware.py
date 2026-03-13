import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("app.middleware")


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # Respect proxy headers (Render, nginx, etc.)
        forwarded_for = request.headers.get("x-forwarded-for")
        client_ip = (
            forwarded_for.split(",")[0].strip()
            if forwarded_for
            else (request.client.host if request.client else "unknown")
        )

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000

            level = logging.WARNING if response.status_code >= 400 else logging.INFO
            logger.log(
                level,
                "%s %s | IP: %s | Status: %d | Time: %.2fms",
                request.method,
                request.url.path,
                client_ip,
                response.status_code,
                process_time,
            )
            return response

        except Exception as exc:
            process_time = (time.time() - start_time) * 1000
            logger.critical(
                "%s %s | IP: %s | UNHANDLED EXCEPTION after %.2fms | %s: %s",
                request.method,
                request.url.path,
                client_ip,
                process_time,
                type(exc).__name__,
                exc,
                exc_info=True,
            )
            raise
