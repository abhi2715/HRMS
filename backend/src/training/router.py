"""
Training module — Schemas & API router.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.core.exceptions import NotFoundException
from src.employees.repository import EmployeeRepository
from src.training.models import TrainingCourse, CourseEnrollment, LearningPath


# ── Schemas ──────────────────────────────────────────────────

class CourseResponse(BaseModel):
    id: uuid.UUID
    title: str
    category: str
    difficulty_level: str
    duration_hours: int
    description: str | None
    is_mandatory: bool
    is_active: bool
    model_config = {"from_attributes": True}


class EnrollmentResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    course_title: str | None = None
    employee_id: uuid.UUID
    status: str
    progress: int
    score: int | None
    started_at: datetime | None
    completed_at: datetime | None
    model_config = {"from_attributes": True}


class TrainingProgramResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    estimated_hours: int | None
    is_active: bool
    model_config = {"from_attributes": True}


class EnrollRequest(BaseModel):
    course_id: uuid.UUID


# ── Router ───────────────────────────────────────────────────

router = APIRouter(prefix="/training", tags=["Training"])


@router.get("/courses", response_model=list[CourseResponse], summary="List courses")
async def list_courses(
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(TrainingCourse).where(TrainingCourse.is_deleted == False, TrainingCourse.is_active == True)
    if category:
        stmt = stmt.where(TrainingCourse.category == category)
    stmt = stmt.order_by(TrainingCourse.title)
    result = await db.execute(stmt)
    courses = list(result.scalars().all())
    return [CourseResponse.model_validate(c) for c in courses]


@router.get("/my-enrollments", response_model=list[EnrollmentResponse], summary="My enrollments")
async def my_enrollments(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    stmt = (
        select(CourseEnrollment)
        .where(CourseEnrollment.employee_id == emp.id, CourseEnrollment.is_deleted == False)
        .order_by(CourseEnrollment.created_at.desc())
    )
    result = await db.execute(stmt)
    enrollments = list(result.scalars().all())

    items = []
    for e in enrollments:
        course = await db.get(TrainingCourse, e.course_id)
        items.append(EnrollmentResponse(
            id=e.id, course_id=e.course_id,
            course_title=course.title if course else None,
            employee_id=e.employee_id, status=e.status,
            progress=e.progress, score=e.score,
            started_at=e.started_at, completed_at=e.completed_at,
        ))
    return items


@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED,
             summary="Enroll in course")
async def enroll(
    data: EnrollRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    course = await db.get(TrainingCourse, data.course_id)
    if not course:
        raise NotFoundException("Course", data.course_id)

    enrollment = CourseEnrollment(
        course_id=data.course_id,
        employee_id=emp.id,
        status="enrolled",
        progress=0,
    )
    db.add(enrollment)
    await db.flush()
    await db.refresh(enrollment)

    return EnrollmentResponse(
        id=enrollment.id, course_id=enrollment.course_id,
        course_title=course.title, employee_id=enrollment.employee_id,
        status=enrollment.status, progress=enrollment.progress,
        score=enrollment.score, started_at=enrollment.started_at,
        completed_at=enrollment.completed_at,
    )


@router.get("/programs", response_model=list[TrainingProgramResponse], summary="Training programs")
async def list_programs(db: AsyncSession = Depends(get_db)):
    stmt = select(LearningPath).where(LearningPath.is_deleted == False).order_by(LearningPath.created_at.desc())
    result = await db.execute(stmt)
    programs = list(result.scalars().all())
    return [TrainingProgramResponse.model_validate(p) for p in programs]


@router.get("/dashboard", summary="Training dashboard",
            dependencies=[Depends(PermissionChecker("training:read"))])
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    total_courses = (await db.execute(
        select(func.count(TrainingCourse.id)).where(TrainingCourse.is_deleted == False, TrainingCourse.is_active == True)
    )).scalar() or 0

    total_enrollments = (await db.execute(
        select(func.count(CourseEnrollment.id)).where(CourseEnrollment.is_deleted == False)
    )).scalar() or 0

    completed = (await db.execute(
        select(func.count(CourseEnrollment.id)).where(CourseEnrollment.status == "completed", CourseEnrollment.is_deleted == False)
    )).scalar() or 0

    in_progress = (await db.execute(
        select(func.count(CourseEnrollment.id)).where(CourseEnrollment.status == "in_progress", CourseEnrollment.is_deleted == False)
    )).scalar() or 0

    return {
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "completed": completed,
        "in_progress": in_progress,
        "completion_rate": round((completed / total_enrollments * 100), 1) if total_enrollments > 0 else 0,
    }
