"""
Auth module — API router with all authentication endpoints.
"""

import uuid

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)
from src.auth.service import AuthService
from src.core.database import get_db
from src.core.dependencies import (
    PermissionChecker,
    get_current_user_id,
    get_current_user_role,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _get_client_ip(request: Request) -> str | None:
    """Extract client IP from the request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(
    data: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user account and return authentication tokens."""
    service = AuthService(db)
    return await service.register(data, ip_address=_get_client_ip(request))


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email and password",
)
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate user credentials and return JWT tokens."""
    service = AuthService(db)
    return await service.login(data, ip_address=_get_client_ip(request))


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Generate a new access token using a valid refresh token."""
    service = AuthService(db)
    return await service.refresh_token(data.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_profile(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Return the authenticated user's profile."""
    service = AuthService(db)
    return await service.get_profile(user_id)


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_profile(
    data: UpdateProfileRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update the authenticated user's profile fields."""
    service = AuthService(db)
    return await service.update_profile(user_id, data)


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="Change password",
)
async def change_password(
    data: ChangePasswordRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Change the authenticated user's password."""
    service = AuthService(db)
    await service.change_password(user_id, data)
    return MessageResponse(message="Password changed successfully")


@router.get(
    "/users",
    summary="List all users (admin)",
    dependencies=[Depends(PermissionChecker("users:*"))],
)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: str | None = Query(None),
    search: str | None = Query(None),
    is_active: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List all users with pagination and filters. Requires admin permissions."""
    service = AuthService(db)
    return await service.list_users(
        page=page, page_size=page_size, role=role, search=search, is_active=is_active
    )


@router.post(
    "/users/{user_id}/deactivate",
    response_model=MessageResponse,
    summary="Deactivate a user (admin)",
    dependencies=[Depends(PermissionChecker("users:*"))],
)
async def deactivate_user(
    user_id: uuid.UUID,
    admin_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Deactivate a user account. Requires admin permissions."""
    service = AuthService(db)
    await service.deactivate_user(user_id, admin_id)
    return MessageResponse(message="User deactivated successfully")
