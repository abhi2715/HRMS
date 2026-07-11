"""
Performance module — Business logic & API router.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.core.exceptions import NotFoundException
from src.employees.repository import EmployeeRepository
from src.performance.models import PerformanceGoal
from src.performance.repository import GoalRepository, PerformanceReviewRepository
from src.performance.schemas import (
    GoalCreateRequest, GoalProgressUpdate, GoalResponse,
    PerformanceReviewResponse,
)

router = APIRouter(prefix="/performance", tags=["Performance"])


# ── Goals ────────────────────────────────────────────────────

@router.get("/goals/my", response_model=list[GoalResponse], summary="My goals")
async def get_my_goals(
    period: str | None = Query(None),
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    repo = GoalRepository(db)
    goals = await repo.get_by_employee(emp.id, period)
    return [GoalResponse.model_validate(g) for g in goals]


@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED,
             summary="Create goal")
async def create_goal(
    data: GoalCreateRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    repo = GoalRepository(db)
    goal = PerformanceGoal(
        employee_id=emp.id,
        title=data.title,
        description=data.description,
        category=data.category,
        review_period=data.period,
        year=2026,
        start_date=data.target_date or date.today(),
        due_date=data.target_date or date.today(),
        weight=data.weight,
        progress=0,
        status="in_progress",
    )
    goal = await repo.create(goal)
    return GoalResponse.model_validate(goal)


@router.patch("/goals/{goal_id}/progress", response_model=GoalResponse, summary="Update goal progress")
async def update_progress(
    goal_id: uuid.UUID,
    data: GoalProgressUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goal = await repo.get_by_id(goal_id)
    if not goal:
        raise NotFoundException("Goal", goal_id)
    goal.progress = data.progress
    if data.progress >= 100:
        goal.status = "completed"
    await db.flush()
    await db.refresh(goal)
    return GoalResponse.model_validate(goal)


# ── Reviews ──────────────────────────────────────────────────

@router.get("/reviews/my", response_model=list[PerformanceReviewResponse], summary="My reviews")
async def get_my_reviews(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    repo = PerformanceReviewRepository(db)
    reviews = await repo.get_by_employee(emp.id)
    return [PerformanceReviewResponse.model_validate(r) for r in reviews]





@router.get("/dashboard", summary="Performance dashboard",
            dependencies=[Depends(PermissionChecker("performance:read"))])
async def get_dashboard(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    goal_repo = GoalRepository(db)
    review_repo = PerformanceReviewRepository(db)

    goal_counts = await goal_repo.count_by_status(emp.id)
    goals = await goal_repo.get_by_employee(emp.id)
    reviews = await review_repo.get_by_employee(emp.id)

    avg_progress = sum(g.progress for g in goals) / len(goals) if goals else 0
    latest_rating = reviews[0].final_rating if reviews and reviews[0].final_rating else None

    return {
        "goal_counts": goal_counts,
        "total_goals": len(goals),
        "avg_progress": round(avg_progress, 1),
        "latest_rating": float(latest_rating) if latest_rating else None,
        "total_reviews": len(reviews),
    }
