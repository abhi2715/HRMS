"""
Leave module — API router.
"""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.employees.repository import EmployeeRepository
from src.leaves.schemas import (
    HolidayResponse, LeaveApprovalRequest, LeaveBalanceResponse,
    LeaveRequestCreate, LeaveRequestResponse, LeaveTypeResponse,
)
from src.leaves.service import LeaveService

router = APIRouter(prefix="/leaves", tags=["Leaves"])


@router.get("/types", response_model=list[LeaveTypeResponse], summary="List leave types")
async def get_leave_types(db: AsyncSession = Depends(get_db)):
    service = LeaveService(db)
    return await service.get_leave_types()


@router.get("/my-balance", response_model=list[LeaveBalanceResponse], summary="Get my leave balance")
async def get_my_balance(
    year: int | None = Query(None),
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp_repo = EmployeeRepository(db)
    emp = await emp_repo.get_by_user_id(user_id)
    service = LeaveService(db)
    return await service.get_my_balances(emp.id, year)


@router.post("/apply", response_model=LeaveRequestResponse, summary="Apply for leave")
async def apply_leave(
    data: LeaveRequestCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp_repo = EmployeeRepository(db)
    emp = await emp_repo.get_by_user_id(user_id)
    service = LeaveService(db)
    return await service.apply_leave(emp.id, data)


@router.get("/my-requests", summary="Get my leave requests")
async def get_my_requests(
    year: int | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp_repo = EmployeeRepository(db)
    emp = await emp_repo.get_by_user_id(user_id)
    service = LeaveService(db)
    return await service.get_my_requests(emp.id, year=year, status=status, page=page, page_size=page_size)


@router.get(
    "/pending-approvals",
    summary="Get pending leave approvals",
    dependencies=[Depends(PermissionChecker("leaves:approve"))],
)
async def get_pending_approvals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = LeaveService(db)
    return await service.get_pending_approvals(page, page_size)


@router.post(
    "/{request_id}/action",
    response_model=LeaveRequestResponse,
    summary="Approve or reject leave",
    dependencies=[Depends(PermissionChecker("leaves:approve"))],
)
async def approve_or_reject(
    request_id: uuid.UUID,
    data: LeaveApprovalRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = LeaveService(db)
    return await service.approve_or_reject(
        request_id, data.action, approved_by=user_id, rejection_reason=data.rejection_reason,
    )


@router.get("/holidays", response_model=list[HolidayResponse], summary="Get holidays")
async def get_holidays(
    year: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = LeaveService(db)
    return await service.get_holidays(year)
