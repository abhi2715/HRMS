"""
Auth module — Pydantic schemas for request/response validation.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.core.security import UserRole


# ── Request Schemas ──────────────────────────────────────────

class RegisterRequest(BaseModel):
    """User registration payload."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: str | None = Field(None, max_length=20)
    role: UserRole = UserRole.EMPLOYEE

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class LoginRequest(BaseModel):
    """User login payload."""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Token refresh payload."""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Password change payload."""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class UpdateProfileRequest(BaseModel):
    """Profile update payload."""
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    phone: str | None = Field(None, max_length=20)
    avatar_url: str | None = None


# ── Response Schemas ─────────────────────────────────────────

class UserResponse(BaseModel):
    """User data returned to the client."""
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    full_name: str
    phone: str | None
    avatar_url: str | None
    primary_role: UserRole
    is_active: bool
    is_verified: bool
    last_login: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("full_name", mode="before")
    @classmethod
    def compute_full_name(cls, v, info):
        if v:
            return v
        first = info.data.get("first_name", "")
        last = info.data.get("last_name", "")
        return f"{first} {last}".strip()


class TokenResponse(BaseModel):
    """JWT token pair returned on login/refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response."""
    success: bool = True
    message: str


# ── Paginated Response ───────────────────────────────────────

class PaginatedResponse(BaseModel):
    """Generic paginated list response."""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1
