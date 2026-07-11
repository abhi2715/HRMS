"""
Payroll module — Pydantic schemas, repository, service, and router.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# ── Schemas ──────────────────────────────────────────────────

class PayrollRunCreate(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2020)
    description: str | None = None


class PayrollRunResponse(BaseModel):
    id: uuid.UUID
    month: int
    year: int
    status: str
    total_employees: int
    total_gross: Decimal
    total_deductions: Decimal
    total_net: Decimal
    processed_by_name: str | None = None
    processed_at: datetime | None
    created_at: datetime
    model_config = {"from_attributes": True}


class PayslipResponse(BaseModel):
    id: uuid.UUID
    payroll_run_id: uuid.UUID
    employee_id: uuid.UUID
    employee_name: str | None = None
    employee_code: str | None = None
    month: int
    year: int
    basic_salary: Decimal
    hra: Decimal
    special_allowance: Decimal
    dearness_allowance: Decimal
    gross_salary: Decimal
    pf_employee: Decimal
    pf_employer: Decimal
    professional_tax: Decimal
    income_tax: Decimal
    total_deductions: Decimal
    net_salary: Decimal
    status: str
    model_config = {"from_attributes": True}


class SalaryStructureResponse(BaseModel):
    id: uuid.UUID
    name: str
    basic_pct: Decimal
    hra_pct: Decimal
    special_pct: Decimal
    da_pct: Decimal
    pf_pct: Decimal
    is_active: bool
    model_config = {"from_attributes": True}
