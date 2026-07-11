"""
Leave module — Pydantic schemas.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LeaveTypeResponse(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    max_days_per_year: int
    is_paid: bool
    is_carry_forward: bool
    max_carry_forward_days: int
    color: str | None
    is_active: bool
    model_config = {"from_attributes": True}


class LeaveBalanceResponse(BaseModel):
    id: uuid.UUID
    leave_type: LeaveTypeResponse
    year: int
    allocated: Decimal
    used: Decimal
    pending: Decimal
    available: Decimal
    model_config = {"from_attributes": True}


class LeaveRequestCreate(BaseModel):
    leave_type_id: uuid.UUID
    start_date: date
    end_date: date
    reason: str = Field(..., min_length=5, max_length=500)
    is_half_day: bool = False
    half_day_period: str | None = None


class LeaveRequestResponse(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    employee_name: str | None = None
    leave_type_name: str | None = None
    leave_type_color: str | None = None
    start_date: date
    end_date: date
    total_days: Decimal
    reason: str
    status: str
    is_half_day: bool
    approved_by_name: str | None = None
    rejection_reason: str | None = None
    ai_recommendation: str | None = None
    ai_risk_score: Decimal | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


class LeaveApprovalRequest(BaseModel):
    action: str = Field(..., pattern="^(approve|reject)$")
    rejection_reason: str | None = None


class HolidayResponse(BaseModel):
    id: uuid.UUID
    name: str
    date: date
    type: str
    year: int
    model_config = {"from_attributes": True}
