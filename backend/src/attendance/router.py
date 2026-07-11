"""
Attendance module — API router.
"""

import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.attendance.schemas import (
    AttendanceRecordResponse, AttendanceSummary,
    CheckInRequest, CheckOutRequest, ShiftResponse,
)
from src.attendance.service import AttendanceService
from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.employees.repository import EmployeeRepository

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/check-in", response_model=AttendanceRecordResponse, summary="Check in")
async def check_in(
    data: CheckInRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    service = AttendanceService(db)
    return await service.check_in(emp.id, data)


@router.post("/check-out", response_model=AttendanceRecordResponse, summary="Check out")
async def check_out(
    data: CheckOutRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    service = AttendanceService(db)
    return await service.check_out(emp.id, data)


@router.get("/my-attendance", response_model=list[AttendanceRecordResponse], summary="My attendance")
async def get_my_attendance(
    from_date: date = Query(default=None),
    to_date: date = Query(default=None),
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if not from_date:
        from_date = date.today().replace(day=1)
    if not to_date:
        to_date = date.today()
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    service = AttendanceService(db)
    return await service.get_my_attendance(emp.id, from_date, to_date)


@router.get("/my-summary", response_model=AttendanceSummary, summary="My summary")
async def get_my_summary(
    from_date: date = Query(default=None),
    to_date: date = Query(default=None),
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if not from_date:
        from_date = date.today().replace(day=1)
    if not to_date:
        to_date = date.today()
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    service = AttendanceService(db)
    return await service.get_my_summary(emp.id, from_date, to_date)


@router.get(
    "/today",
    summary="Today's attendance overview",
    dependencies=[Depends(PermissionChecker("attendance:read"))],
)
async def today_overview(db: AsyncSession = Depends(get_db)):
    service = AttendanceService(db)
    return await service.get_today_overview()


@router.get("/shifts", response_model=list[ShiftResponse], summary="List shifts")
async def get_shifts(db: AsyncSession = Depends(get_db)):
    service = AttendanceService(db)
    return await service.get_shifts()
