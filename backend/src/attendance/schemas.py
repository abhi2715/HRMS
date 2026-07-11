"""
Attendance module — Pydantic schemas.
"""

import uuid
from datetime import date, datetime, time
from decimal import Decimal

from pydantic import BaseModel, Field


class ShiftResponse(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    start_time: time
    end_time: time
    grace_minutes: int
    is_night_shift: bool
    color: str | None
    model_config = {"from_attributes": True}


class AttendanceRecordResponse(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    employee_name: str | None = None
    date: date
    check_in: datetime | None
    check_out: datetime | None
    status: str
    work_hours: Decimal | None
    overtime_hours: Decimal | None
    is_late: bool
    late_minutes: int
    is_remote: bool
    location_lat: float | None
    location_lng: float | None
    model_config = {"from_attributes": True}


class CheckInRequest(BaseModel):
    location_lat: float | None = None
    location_lng: float | None = None
    is_remote: bool = False


class CheckOutRequest(BaseModel):
    location_lat: float | None = None
    location_lng: float | None = None


class AttendanceSummary(BaseModel):
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    leave_days: int
    wfh_days: int
    avg_work_hours: Decimal
    total_overtime: Decimal
    attendance_percentage: Decimal
