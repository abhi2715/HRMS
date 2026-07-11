"""
Auth module — Business logic for authentication and user management.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.repository import AuditLogRepository, UserRepository
from src.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)
from src.core.config import get_settings
from src.core.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

settings = get_settings()


class AuthService:
    """Business logic for authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditLogRepository(db)

    async def register(self, data: RegisterRequest, ip_address: str | None = None) -> TokenResponse:
        """Register a new user account."""
        # Check if email already exists
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise AlreadyExistsException("User", "email", data.email)

        # Create user
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            primary_role=data.role,
            is_active=True,
            is_verified=False,
        )
        user = await self.user_repo.create(user)

        # Audit log
        await self.audit_repo.create(
            action="user.registered",
            resource_type="user",
            resource_id=str(user.id),
            user_id=user.id,
            ip_address=ip_address,
            details=f"User registered with role {data.role.value}",
        )

        # Generate tokens
        return self._create_token_response(user)

    async def login(self, data: LoginRequest, ip_address: str | None = None) -> TokenResponse:
        """Authenticate a user and return tokens."""
        user = await self.user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated. Contact your HR administrator.")

        # Update last login
        await self.user_repo.update(user.id, last_login=datetime.now(timezone.utc))

        # Audit log
        await self.audit_repo.create(
            action="user.login",
            resource_type="user",
            resource_id=str(user.id),
            user_id=user.id,
            ip_address=ip_address,
        )

        return self._create_token_response(user)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Generate new access token using a valid refresh token."""
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise UnauthorizedException("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid token type")

        user_id = uuid.UUID(payload["sub"])
        user = await self.user_repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise UnauthorizedException("User not found or deactivated")

        return self._create_token_response(user)

    async def get_profile(self, user_id: uuid.UUID) -> UserResponse:
        """Get the current user's profile."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return UserResponse.model_validate(user)

    async def update_profile(
        self, user_id: uuid.UUID, data: UpdateProfileRequest
    ) -> UserResponse:
        """Update the current user's profile."""
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationException("No fields to update")

        user = await self.user_repo.update(user_id, **update_data)
        if not user:
            raise NotFoundException("User", user_id)

        return UserResponse.model_validate(user)

    async def change_password(
        self, user_id: uuid.UUID, data: ChangePasswordRequest
    ) -> None:
        """Change the user's password."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)

        if not verify_password(data.current_password, user.hashed_password):
            raise UnauthorizedException("Current password is incorrect")

        new_hash = hash_password(data.new_password)
        await self.user_repo.update(user_id, hashed_password=new_hash)

        await self.audit_repo.create(
            action="user.password_changed",
            resource_type="user",
            resource_id=str(user_id),
            user_id=user_id,
        )

    async def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        role: str | None = None,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> dict:
        """List users with pagination and filters (admin only)."""
        from src.core.security import UserRole as RoleEnum

        role_enum = RoleEnum(role) if role else None
        users, total = await self.user_repo.get_all(
            page=page,
            page_size=page_size,
            role=role_enum,
            search=search,
            is_active=is_active,
        )

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": [UserResponse.model_validate(u) for u in users],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    async def deactivate_user(self, user_id: uuid.UUID, admin_id: uuid.UUID) -> None:
        """Deactivate a user account (admin only)."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)

        await self.user_repo.update(user_id, is_active=False)

        await self.audit_repo.create(
            action="user.deactivated",
            resource_type="user",
            resource_id=str(user_id),
            user_id=admin_id,
            details=f"User {user.email} deactivated by admin",
        )

    def _create_token_response(self, user: User) -> TokenResponse:
        """Helper to create a JWT token pair response."""
        access_token = create_access_token(
            subject=user.id,
            role=user.primary_role.value if isinstance(user.primary_role, str) is False else user.primary_role,
            extra_claims={"email": user.email, "name": user.full_name},
        )
        refresh = create_refresh_token(subject=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )
