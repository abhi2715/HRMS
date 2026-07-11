"""
Employee module — Pydantic schemas for request/response validation.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# ── Request Schemas ──────────────────────────────────────────

class EmployeeCreateRequest(BaseModel):
    """Create a new employee."""
    user_id: uuid.UUID | None = None
    email: str = Field(..., max_length=255)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str | None = Field(None, min_length=8)
    employee_code: str = Field(..., max_length=20)
    department_id: uuid.UUID | None = None
    designation_id: uuid.UUID | None = None
    reporting_manager_id: uuid.UUID | None = None
    employment_type: str = "full_time"
    date_of_birth: date | None = None
    gender: str | None = None
    marital_status: str | None = None
    blood_group: str | None = None
    nationality: str = "Indian"
    personal_email: str | None = None
    work_phone: str | None = None
    personal_phone: str | None = None
    current_address: str | None = None
    permanent_address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str = "India"
    pin_code: str | None = None
    date_of_joining: date
    ctc: Decimal | None = None
    basic_salary: Decimal | None = None
    bank_name: str | None = None
    bank_account_number: str | None = None
    ifsc_code: str | None = None
    pan_number: str | None = None
    uan_number: str | None = None
    work_location: str = "Office"


class EmployeeUpdateRequest(BaseModel):
    """Update employee fields."""
    department_id: uuid.UUID | None = None
    designation_id: uuid.UUID | None = None
    reporting_manager_id: uuid.UUID | None = None
    employment_type: str | None = None
    employment_status: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    marital_status: str | None = None
    blood_group: str | None = None
    personal_email: str | None = None
    work_phone: str | None = None
    personal_phone: str | None = None
    current_address: str | None = None
    permanent_address: str | None = None
    city: str | None = None
    state: str | None = None
    pin_code: str | None = None
    ctc: Decimal | None = None
    basic_salary: Decimal | None = None
    bank_name: str | None = None
    bank_account_number: str | None = None
    ifsc_code: str | None = None
    pan_number: str | None = None
    uan_number: str | None = None
    work_location: str | None = None


class DepartmentCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    description: str | None = None
    head_id: uuid.UUID | None = None
    parent_id: uuid.UUID | None = None
    color: str | None = None


class DesignationCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    level: int = Field(1, ge=1, le=10)
    description: str | None = None


class SkillRequest(BaseModel):
    skill_name: str = Field(..., max_length=100)
    category: str | None = None
    proficiency: int = Field(3, ge=1, le=5)
    years_experience: int | None = None
    is_primary: bool = False


# ── Response Schemas ─────────────────────────────────────────

class DepartmentResponse(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    description: str | None
    color: str | None
    is_active: bool
    employee_count: int | None = None
    head_name: str | None = None

    model_config = {"from_attributes": True}


class DesignationResponse(BaseModel):
    id: uuid.UUID
    title: str
    level: int
    description: str | None
    is_active: bool

    model_config = {"from_attributes": True}


class SkillResponse(BaseModel):
    id: uuid.UUID
    skill_name: str
    category: str | None
    proficiency: int
    years_experience: int | None
    is_primary: bool

    model_config = {"from_attributes": True}


class EmployeeListResponse(BaseModel):
    """Lightweight employee for list views."""
    id: uuid.UUID
    employee_code: str
    user_id: uuid.UUID
    first_name: str
    last_name: str
    full_name: str
    email: str
    avatar_url: str | None
    department_name: str | None
    designation_title: str | None
    employment_type: str
    employment_status: str
    date_of_joining: date
    work_location: str
    city: str | None

    model_config = {"from_attributes": True}


class EmployeeDetailResponse(BaseModel):
    """Full employee profile."""
    id: uuid.UUID
    employee_code: str
    user_id: uuid.UUID
    first_name: str
    last_name: str
    full_name: str
    email: str
    avatar_url: str | None
    phone: str | None

    # Department & Designation
    department: DepartmentResponse | None
    designation: DesignationResponse | None
    reporting_manager_name: str | None

    # Employment
    employment_type: str
    employment_status: str
    date_of_joining: date
    date_of_confirmation: date | None
    date_of_exit: date | None
    notice_period_days: int

    # Personal
    date_of_birth: date | None
    gender: str | None
    marital_status: str | None
    blood_group: str | None
    nationality: str

    # Contact
    personal_email: str | None
    work_phone: str | None
    personal_phone: str | None

    # Address
    current_address: str | None
    permanent_address: str | None
    city: str | None
    state: str | None
    country: str
    pin_code: str | None

    # Compensation
    ctc: Decimal | None
    basic_salary: Decimal | None
    bank_name: str | None
    pan_number: str | None

    # Work
    work_location: str
    shift: str

    # AI
    ai_summary: str | None

    # Relations
    skills: list[SkillResponse]

    created_at: datetime

    model_config = {"from_attributes": True}
