"""
Recruitment module — Pydantic schemas.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class JobPostingCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    department_id: uuid.UUID | None = None
    description: str = Field(..., min_length=20)
    requirements: str | None = None
    required_skills: list[str] | None = None
    experience_min: int | None = None
    experience_max: int | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    location: str = "Bangalore"
    job_type: str = "full_time"
    positions: int = 1


class JobPostingResponse(BaseModel):
    id: uuid.UUID
    title: str
    department_name: str | None = None
    description: str
    requirements: str | None
    required_skills: list[str] | None
    experience_min: int | None
    experience_max: int | None
    salary_min: Decimal | None
    salary_max: Decimal | None
    location: str
    job_type: str
    positions: int
    status: str
    total_applicants: int = 0
    posted_at: datetime | None
    created_at: datetime
    model_config = {"from_attributes": True}


class CandidateResponse(BaseModel):
    id: uuid.UUID
    job_posting_id: uuid.UUID
    job_title: str | None = None
    first_name: str
    last_name: str
    full_name: str | None = None
    email: str
    phone: str | None
    experience_years: int | None
    current_ctc: Decimal | None
    expected_ctc: Decimal | None
    notice_period_days: int | None
    source: str | None
    stage: str
    ai_score: Decimal | None
    ai_evaluation: str | None
    skills_extracted: list[str] | None
    created_at: datetime
    model_config = {"from_attributes": True}


class CandidateCreateRequest(BaseModel):
    job_posting_id: uuid.UUID
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: str
    phone: str | None = None
    experience_years: int | None = None
    current_ctc: Decimal | None = None
    expected_ctc: Decimal | None = None
    notice_period_days: int | None = None
    source: str = "website"
    skills_extracted: list[str] | None = None


class CandidateStageUpdate(BaseModel):
    stage: str = Field(..., pattern="^(applied|screening|shortlisted|interview|technical|hr_round|offer|hired|rejected)$")
    notes: str | None = None


class RecruitmentDashboard(BaseModel):
    total_open_positions: int
    total_applicants: int
    shortlisted: int
    interviews_scheduled: int
    offers_sent: int
    pipeline_by_stage: dict[str, int]
    top_sources: list[dict]
