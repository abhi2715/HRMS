"""
Leave module — Business logic.
"""

import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException, ValidationException
from src.employees.repository import EmployeeRepository
from src.leaves.models import LeaveRequest
from src.leaves.repository import (
    HolidayRepository, LeaveBalanceRepository,
    LeaveRequestRepository, LeaveTypeRepository,
)
from src.leaves.schemas import (
    HolidayResponse, LeaveBalanceResponse, LeaveRequestCreate,
    LeaveRequestResponse, LeaveTypeResponse,
)


class LeaveService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.type_repo = LeaveTypeRepository(db)
        self.balance_repo = LeaveBalanceRepository(db)
        self.request_repo = LeaveRequestRepository(db)
        self.holiday_repo = HolidayRepository(db)
        self.employee_repo = EmployeeRepository(db)

    async def get_leave_types(self) -> list[LeaveTypeResponse]:
        types = await self.type_repo.get_all()
        return [LeaveTypeResponse.model_validate(t) for t in types]

    async def get_my_balances(self, employee_id: uuid.UUID, year: int = None) -> list[LeaveBalanceResponse]:
        if year is None:
            year = date.today().year
        balances = await self.balance_repo.get_by_employee_year(employee_id, year)
        result = []
        for b in balances:
            available = b.allocated - b.used - b.pending
            result.append(LeaveBalanceResponse(
                id=b.id,
                leave_type=LeaveTypeResponse.model_validate(b.leave_type),
                year=b.year,
                allocated=b.allocated,
                used=b.used,
                pending=b.pending,
                available=max(Decimal(0), available),
            ))
        return result

    async def apply_leave(self, employee_id: uuid.UUID, data: LeaveRequestCreate) -> LeaveRequestResponse:
        # Validate dates
        if data.end_date < data.start_date:
            raise ValidationException("End date must be after start date")

        # Calculate days
        total_days = Decimal(str((data.end_date - data.start_date).days + 1))
        if data.is_half_day:
            total_days = Decimal("0.5")

        # Check leave type
        leave_type = await self.type_repo.get_by_id(data.leave_type_id)
        if not leave_type:
            raise NotFoundException("Leave Type", data.leave_type_id)

        # Check balance
        balance = await self.balance_repo.get_for_type(
            employee_id, data.leave_type_id, data.start_date.year,
        )
        if balance:
            available = balance.allocated - balance.used - balance.pending
            if total_days > available and leave_type.code != "LOP":
                raise ValidationException(
                    f"Insufficient leave balance. Available: {available}, Requested: {total_days}"
                )
            # Update pending balance
            balance.pending = balance.pending + total_days
            await self.db.flush()

        # Create request
        leave_req = LeaveRequest(
            employee_id=employee_id,
            leave_type_id=data.leave_type_id,
            start_date=data.start_date,
            end_date=data.end_date,
            total_days=total_days,
            reason=data.reason,
            status="pending",
            is_half_day=data.is_half_day,
            half_day_period=data.half_day_period,
        )
        leave_req = await self.request_repo.create(leave_req)

        return self._to_response(leave_req, leave_type_name=leave_type.name, leave_type_color=leave_type.color)

    async def get_my_requests(
        self, employee_id: uuid.UUID, year: int | None = None,
        status: str | None = None, page: int = 1, page_size: int = 20,
    ) -> dict:
        requests, total = await self.request_repo.get_by_employee(
            employee_id, year=year, status=status, page=page, page_size=page_size,
        )
        items = [self._to_response(r, leave_type_name=r.leave_type.name if r.leave_type else None,
                                    leave_type_color=r.leave_type.color if r.leave_type else None) for r in requests]
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_pending_approvals(self, page: int = 1, page_size: int = 20) -> dict:
        requests, total = await self.request_repo.get_pending_for_approval(page, page_size)
        items = []
        for r in requests:
            emp = await self.employee_repo.get_by_id(r.employee_id)
            name = emp.user.full_name if emp and emp.user else "Unknown"
            items.append(self._to_response(
                r,
                employee_name=name,
                leave_type_name=r.leave_type.name if r.leave_type else None,
                leave_type_color=r.leave_type.color if r.leave_type else None,
            ))
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def approve_or_reject(
        self, request_id: uuid.UUID, action: str,
        approved_by: uuid.UUID, rejection_reason: str | None = None,
    ) -> LeaveRequestResponse:
        leave_req = await self.request_repo.get_by_id(request_id)
        if not leave_req:
            raise NotFoundException("Leave Request", request_id)
        if leave_req.status != "pending":
            raise ValidationException(f"Leave request is already {leave_req.status}")

        # Update balance
        balance = await self.balance_repo.get_for_type(
            leave_req.employee_id, leave_req.leave_type_id, leave_req.start_date.year,
        )
        if balance:
            balance.pending = max(Decimal(0), balance.pending - leave_req.total_days)
            if action == "approve":
                balance.used = balance.used + leave_req.total_days
            await self.db.flush()

        leave_req.status = "approved" if action == "approve" else "rejected"
        leave_req.approved_by = approved_by if action == "approve" else None
        leave_req.rejection_reason = rejection_reason
        await self.db.flush()
        await self.db.refresh(leave_req)

        return self._to_response(leave_req,
                                  leave_type_name=leave_req.leave_type.name if leave_req.leave_type else None,
                                  leave_type_color=leave_req.leave_type.color if leave_req.leave_type else None)

    async def get_holidays(self, year: int = None) -> list[HolidayResponse]:
        if not year:
            year = date.today().year
        holidays = await self.holiday_repo.get_by_year(year)
        return [HolidayResponse.model_validate(h) for h in holidays]

    async def count_pending(self) -> int:
        return await self.request_repo.count_pending()

    def _to_response(
        self, lr: LeaveRequest, employee_name: str | None = None,
        leave_type_name: str | None = None, leave_type_color: str | None = None,
    ) -> LeaveRequestResponse:
        return LeaveRequestResponse(
            id=lr.id,
            employee_id=lr.employee_id,
            employee_name=employee_name,
            leave_type_name=leave_type_name,
            leave_type_color=leave_type_color,
            start_date=lr.start_date,
            end_date=lr.end_date,
            total_days=lr.total_days,
            reason=lr.reason,
            status=lr.status,
            is_half_day=lr.is_half_day,
            rejection_reason=lr.rejection_reason,
            ai_recommendation=lr.ai_recommendation,
            ai_risk_score=lr.ai_risk_score,
            created_at=lr.created_at,
        )
