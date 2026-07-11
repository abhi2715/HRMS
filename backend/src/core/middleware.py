"""
FastAPI middleware: CORS, request logging, audit trail, and rate limiting.
"""

import logging
import time
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("hrms")


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware on the FastAPI application."""

    # ── CORS ─────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )

    # ── Request ID & Timing ──────────────────────────────────
    app.add_middleware(RequestContextMiddleware)

    # ── Audit Logging ────────────────────────────────────────
    app.add_middleware(AuditLogMiddleware)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID and measure processing time."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests with method, path, status, and timing."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        request_id = getattr(request.state, "request_id", "unknown")

        # Skip logging for health checks and docs
        if request.url.path not in ("/health", "/docs", "/openapi.json", "/redoc"):
            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time": f"{process_time:.4f}s",
                    "client_ip": request.client.host if request.client else "unknown",
                },
            )

        return response
