"""
Auth module — Repository layer for user data access.
"""

import uuid

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import AuditLog, User
from src.core.security import UserRole


class UserRepository:
    """Data access layer for User entities."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        """Insert a new user."""
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetch a user by ID (excluding soft-deleted)."""
        stmt = select(User).where(User.id == user_id, User.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email address."""
        stmt = select(User).where(User.email == email, User.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        role: UserRole | None = None,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        """Fetch paginated users with optional filters."""
        stmt = select(User).where(User.is_deleted == False)
        count_stmt = select(func.count(User.id)).where(User.is_deleted == False)

        if role:
            stmt = stmt.where(User.primary_role == role)
            count_stmt = count_stmt.where(User.primary_role == role)

        if search:
            search_filter = (
                User.first_name.ilike(f"%{search}%")
                | User.last_name.ilike(f"%{search}%")
                | User.email.ilike(f"%{search}%")
            )
            stmt = stmt.where(search_filter)
            count_stmt = count_stmt.where(search_filter)

        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
            count_stmt = count_stmt.where(User.is_active == is_active)

        # Get total count
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0

        # Apply pagination
        offset = (page - 1) * page_size
        stmt = stmt.order_by(User.created_at.desc()).offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        users = list(result.scalars().all())

        return users, total

    async def update(self, user_id: uuid.UUID, **kwargs) -> User | None:
        """Update user fields."""
        stmt = (
            update(User)
            .where(User.id == user_id, User.is_deleted == False)
            .values(**kwargs)
            .returning(User)
        )
        result = await self.db.execute(stmt)
        await self.db.flush()
        user = result.scalar_one_or_none()
        if user:
            await self.db.refresh(user)
        return user

    async def soft_delete(self, user_id: uuid.UUID) -> bool:
        """Soft delete a user."""
        user = await self.get_by_id(user_id)
        if user:
            user.soft_delete()
            await self.db.flush()
            return True
        return False

    async def count_by_role(self) -> dict[str, int]:
        """Count users grouped by role."""
        stmt = (
            select(User.primary_role, func.count(User.id))
            .where(User.is_deleted == False, User.is_active == True)
            .group_by(User.primary_role)
        )
        result = await self.db.execute(stmt)
        return {str(role): count for role, count in result.all()}


class AuditLogRepository:
    """Data access layer for audit logs."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        user_id: uuid.UUID | None = None,
        details: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        """Create an audit log entry."""
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(log)
        await self.db.flush()
        return log

    async def get_recent(self, limit: int = 50) -> list[AuditLog]:
        """Fetch the most recent audit logs."""
        stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
