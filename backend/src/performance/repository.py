"""
Performance module — Repository layer.
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.performance.models import PerformanceGoal, PerformanceReview

class GoalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, goal: PerformanceGoal) -> PerformanceGoal:
        self.db.add(goal)
        await self.db.flush()
        await self.db.refresh(goal)
        return goal

    async def get_by_id(self, goal_id: uuid.UUID) -> PerformanceGoal | None:
        stmt = select(PerformanceGoal).where(PerformanceGoal.id == goal_id, PerformanceGoal.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_employee(self, employee_id: uuid.UUID, period: str | None = None) -> list[PerformanceGoal]:
        stmt = select(PerformanceGoal).where(PerformanceGoal.employee_id == employee_id, PerformanceGoal.is_deleted == False)
        if period:
            stmt = stmt.where(PerformanceGoal.review_period == period)
        stmt = stmt.order_by(PerformanceGoal.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_status(self, employee_id: uuid.UUID) -> dict[str, int]:
        stmt = (
            select(PerformanceGoal.status, func.count(PerformanceGoal.id))
            .where(PerformanceGoal.employee_id == employee_id, PerformanceGoal.is_deleted == False)
            .group_by(PerformanceGoal.status)
        )
        result = await self.db.execute(stmt)
        return {status: count for status, count in result.all()}





class PerformanceReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_employee(self, employee_id: uuid.UUID) -> list[PerformanceReview]:
        stmt = (
            select(PerformanceReview)
            .where(PerformanceReview.employee_id == employee_id, PerformanceReview.is_deleted == False)
            .order_by(PerformanceReview.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_team_reviews(self, year: int) -> list[PerformanceReview]:
        stmt = (
            select(PerformanceReview)
            .where(PerformanceReview.year == year, PerformanceReview.is_deleted == False)
            .order_by(PerformanceReview.final_rating.desc().nullslast())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
