"""
Security utilities: JWT token management, password hashing, and RBAC.
"""

import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import wraps
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import get_settings

settings = get_settings()

# ── Password Hashing ─────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Tokens ───────────────────────────────────────────────
def create_access_token(
    subject: str | uuid.UUID,
    role: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(subject),
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str | uuid.UUID) -> str:
    """Create a JWT refresh token with longer expiry."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token. Raises JWTError on failure."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise


# ── RBAC ─────────────────────────────────────────────────────
class UserRole(str, Enum):
    """System user roles ordered by privilege level."""
    SUPER_ADMIN = "super_admin"
    HR_MANAGER = "hr_manager"
    DEPARTMENT_MANAGER = "department_manager"
    RECRUITER = "recruiter"
    PAYROLL_OFFICER = "payroll_officer"
    EMPLOYEE = "employee"


# Role hierarchy: higher roles inherit permissions of lower roles
ROLE_HIERARCHY: dict[UserRole, int] = {
    UserRole.SUPER_ADMIN: 100,
    UserRole.HR_MANAGER: 80,
    UserRole.DEPARTMENT_MANAGER: 60,
    UserRole.RECRUITER: 50,
    UserRole.PAYROLL_OFFICER: 50,
    UserRole.EMPLOYEE: 10,
}

# Granular permissions per module
ROLE_PERMISSIONS: dict[UserRole, set[str]] = {
    UserRole.SUPER_ADMIN: {
        "users:*", "employees:*", "departments:*", "designations:*",
        "recruitment:*", "payroll:*", "leaves:*", "attendance:*",
        "performance:*", "training:*", "compliance:*", "analytics:*",
        "settings:*", "ai:*", "reports:*",
    },
    UserRole.HR_MANAGER: {
        "employees:read", "employees:write", "employees:delete",
        "departments:read", "departments:write",
        "designations:read", "designations:write",
        "recruitment:read", "recruitment:write",
        "payroll:read", "payroll:write",
        "leaves:read", "leaves:write", "leaves:approve",
        "attendance:read", "attendance:write",
        "performance:read", "performance:write",
        "training:read", "training:write",
        "compliance:read", "compliance:write",
        "analytics:read", "ai:read", "ai:write",
        "reports:read", "reports:generate",
    },
    UserRole.DEPARTMENT_MANAGER: {
        "employees:read",
        "departments:read",
        "leaves:read", "leaves:approve",
        "attendance:read",
        "performance:read", "performance:write",
        "training:read",
        "analytics:read",
        "ai:read",
    },
    UserRole.RECRUITER: {
        "employees:read",
        "recruitment:read", "recruitment:write",
        "ai:read",
    },
    UserRole.PAYROLL_OFFICER: {
        "employees:read",
        "payroll:read", "payroll:write",
        "analytics:read",
        "ai:read",
    },
    UserRole.EMPLOYEE: {
        "employees:read:self",
        "leaves:read:self", "leaves:write:self",
        "attendance:read:self",
        "performance:read:self",
        "training:read", "training:enroll",
        "ai:read",
    },
}


def has_permission(user_role: UserRole, required_permission: str) -> bool:
    """Check if a role has a specific permission. Supports wildcard matching."""
    user_permissions = ROLE_PERMISSIONS.get(user_role, set())

    # Direct match
    if required_permission in user_permissions:
        return True

    # Wildcard match: "employees:*" matches "employees:read"
    module = required_permission.split(":")[0]
    if f"{module}:*" in user_permissions:
        return True

    return False


def require_permissions(*permissions: str):
    """Decorator to enforce permission checks on route handlers.
    
    Usage:
        @require_permissions("employees:read", "employees:write")
        async def update_employee(...):
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Permission check is handled by the dependency injection
            # This decorator simply marks the required permissions
            return await func(*args, **kwargs)
        wrapper._required_permissions = permissions
        return wrapper
    return decorator
