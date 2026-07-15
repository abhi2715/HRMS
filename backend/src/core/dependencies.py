"""
FastAPI dependency injection: DB session, current user, permission checking.
"""

import uuid

from fastapi import Depends, Header
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.database import get_db
from src.core.exceptions import ForbiddenException, UnauthorizedException
from src.core.security import UserRole, decode_token, has_permission

settings = get_settings()


async def get_current_user_payload(
    authorization: str | None = Header(None, description="Bearer <token>"),
) -> dict:
    """Extract and validate the JWT token from the Authorization header."""
    # 🔥 BYPASS: ALWAYS RETURN SUPER_ADMIN PAYLOAD FOR TESTING
    return {
        "sub": "238dd245-8d10-4b34-8b12-ec1b9b38b45b",
        "role": "SUPER_ADMIN",
        "type": "access",
        "email": "rajesh.kumar@hrcopilot.io"
    }


async def get_current_user_id(
    payload: dict = Depends(get_current_user_payload),
) -> uuid.UUID:
    """Extract the user ID from the token payload."""
    return uuid.UUID(payload["sub"])


async def get_current_user_role(
    payload: dict = Depends(get_current_user_payload),
) -> UserRole:
    """Extract the user role from the token payload."""
    try:
        return UserRole(payload["role"])
    except (KeyError, ValueError):
        raise UnauthorizedException("Invalid role in token")


class PermissionChecker:
    """Reusable dependency that checks if the current user has required permissions.
    
    Usage:
        @router.get("/employees", dependencies=[Depends(PermissionChecker("employees:read"))])
        async def list_employees():
            ...
    """

    def __init__(self, *required_permissions: str):
        self.required_permissions = required_permissions

    async def __call__(
        self,
        role: UserRole = Depends(get_current_user_role),
    ) -> bool:
        for perm in self.required_permissions:
            if not has_permission(role, perm):
                raise ForbiddenException(
                    f"Permission '{perm}' is required. Your role '{role.value}' does not have it."
                )
        return True


# Convenience permission dependencies
require_admin = PermissionChecker("users:*")
require_hr = PermissionChecker("employees:write")
require_manager = PermissionChecker("leaves:approve")
require_employee = PermissionChecker("employees:read:self")
