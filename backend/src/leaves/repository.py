"""
Leave module — Repository layer.
"""

import uuid
from datetime import date

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.leaves.models import Holiday, LeaveBalance, LeaveRequest, LeaveType


class LeaveTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[LeaveType]:
        stmt = select(LeaveType).where(LeaveType.is_deleted == False).order_by(LeaveType.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, lt_id: uuid.UUID) -> LeaveType | None:
        stmt = select(LeaveType).where(LeaveType.id == lt_id, LeaveType.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class LeaveBalanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_employee_year(self, employee_id: uuid.UUID, year: int) -> list[LeaveBalance]:
        stmt = (
            select(LeaveBalance)
            .options(selectinload(LeaveBalance.leave_type))
            .where(
                LeaveBalance.employee_id == employee_id,
                LeaveBalance.year == year,
                LeaveBalance.is_deleted == False,
            )
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_for_type(self, employee_id: uuid.UUID, leave_type_id: uuid.UUID, year: int) -> LeaveBalance | None:
        stmt = select(LeaveBalance).where(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type_id == leave_type_id,
            LeaveBalance.year == year,
            LeaveBalance.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class LeaveRequestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.add(leave_request)
        await self.db.flush()
        await self.db.refresh(leave_request)
        return leave_request

    async def get_by_id(self, lr_id: uuid.UUID) -> LeaveRequest | None:
        stmt = (
            select(LeaveRequest)
            .options(selectinload(LeaveRequest.leave_type))
            .where(LeaveRequest.id == lr_id, LeaveRequest.is_deleted == False)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_employee(
        self, employee_id: uuid.UUID, year: int | None = None,
        status: str | None = None, page: int = 1, page_size: int = 20,
    ) -> tuple[list[LeaveRequest], int]:
        stmt = (
            select(LeaveRequest)
            .options(selectinload(LeaveRequest.leave_type))
            .where(LeaveRequest.employee_id == employee_id, LeaveRequest.is_deleted == False)
        )
        count_stmt = select(func.count(LeaveRequest.id)).where(
            LeaveRequest.employee_id == employee_id, LeaveRequest.is_deleted == False,
        )

        if year:
            from sqlalchemy import extract
            stmt = stmt.where(extract("year", LeaveRequest.start_date) == year)
            count_stmt = count_stmt.where(extract("year", LeaveRequest.start_date) == year)
        if status:
            stmt = stmt.where(LeaveRequest.status == status)
            count_stmt = count_stmt.where(LeaveRequest.status == status)

        total = (await self.db.execute(count_stmt)).scalar() or 0

        stmt = stmt.order_by(LeaveRequest.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def get_pending_for_approval(
        self, page: int = 1, page_size: int = 20,
    ) -> tuple[list[LeaveRequest], int]:
        stmt = (
            select(LeaveRequest)
            .options(selectinload(LeaveRequest.leave_type))
            .where(LeaveRequest.status == "pending", LeaveRequest.is_deleted == False)
            .order_by(LeaveRequest.created_at.desc())
        )
        count_stmt = select(func.count(LeaveRequest.id)).where(
            LeaveRequest.status == "pending", LeaveRequest.is_deleted == False,
        )
        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def count_pending(self) -> int:
        stmt = select(func.count(LeaveRequest.id)).where(
            LeaveRequest.status == "pending", LeaveRequest.is_deleted == False,
        )
        return (await self.db.execute(stmt)).scalar() or 0


class HolidayRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_year(self, year: int) -> list[Holiday]:
        stmt = (
            select(Holiday)
            .where(Holiday.year == year, Holiday.is_deleted == False)
            .order_by(Holiday.date)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
