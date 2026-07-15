"""
Custom exception hierarchy with FastAPI exception handlers.
"""

import uuid
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource", resource_id: str | uuid.UUID | None = None):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class AlreadyExistsException(AppException):
    """Resource already exists (conflict)."""

    def __init__(self, resource: str = "Resource", field: str = "value", value: str = ""):
        message = f"{resource} with {field} '{value}' already exists"
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


class UnauthorizedException(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationException(AppException):
    """Input validation failed."""

    def __init__(self, message: str = "Validation error", details: Any = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class RateLimitException(AppException):
    """Rate limit exceeded."""

    def __init__(self):
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


class ServiceUnavailableException(AppException):
    """External service unavailable."""

    def __init__(self, service: str = "External service"):
        super().__init__(
            message=f"{service} is currently unavailable. Please try again later.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


# ── Exception Handlers ──────────────────────────────────────

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle all AppException subclasses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "details": exc.details,
            "path": str(request.url),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "path": str(request.url),
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unhandled exceptions."""
    from src.core.config import get_settings
    import traceback
    
    settings = get_settings()
    content = {
        "success": False,
        "message": "An internal server error occurred",
        "path": str(request.url),
    }
    
    if settings.DEBUG:
        content["details"] = str(exc)
        content["traceback"] = traceback.format_exc()
        
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )
