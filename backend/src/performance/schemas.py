"""
Performance module — Schemas, repository, service, and router.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


# ── Schemas ──────────────────────────────────────────────────

class GoalCreateRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str | None = None
    category: str = "individual"
    period: str = "Q2 2026"
    target_date: date | None = None
    weight: int = Field(25, ge=1, le=100)


class GoalResponse(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    title: str
    description: str | None
    category: str
    review_period: str
    year: int
    progress: int
    status: str
    weight: int
    start_date: date
    due_date: date
    created_at: datetime
    model_config = {"from_attributes": True}


class GoalProgressUpdate(BaseModel):
    progress: int = Field(..., ge=0, le=100)
    notes: str | None = None





class PerformanceReviewResponse(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    employee_name: str | None = None
    review_period: str
    year: int
    self_rating: Decimal | None
    manager_rating: Decimal | None
    final_rating: Decimal | None
    status: str
    strengths: str | None
    areas_of_improvement: str | None
    ai_summary: str | None
    created_at: datetime
    model_config = {"from_attributes": True}
