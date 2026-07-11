"""
Recruitment module — Repository layer.
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.recruitment.models import Candidate, CandidateResume, Interview, JobPosting


class JobPostingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, posting: JobPosting) -> JobPosting:
        self.db.add(posting)
        await self.db.flush()
        await self.db.refresh(posting)
        return posting

    async def get_by_id(self, posting_id: uuid.UUID) -> JobPosting | None:
        stmt = select(JobPosting).where(JobPosting.id == posting_id, JobPosting.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self, status: str | None = None, page: int = 1, page_size: int = 20,
    ) -> tuple[list[JobPosting], int]:
        stmt = select(JobPosting).where(JobPosting.is_deleted == False)
        count_stmt = select(func.count(JobPosting.id)).where(JobPosting.is_deleted == False)

        if status:
            stmt = stmt.where(JobPosting.status == status)
            count_stmt = count_stmt.where(JobPosting.status == status)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(JobPosting.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def count_open(self) -> int:
        stmt = select(func.count(JobPosting.id)).where(
            JobPosting.status == "open", JobPosting.is_deleted == False,
        )
        return (await self.db.execute(stmt)).scalar() or 0


class CandidateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, candidate: Candidate) -> Candidate:
        self.db.add(candidate)
        await self.db.flush()
        await self.db.refresh(candidate)
        return candidate

    async def get_by_id(self, cand_id: uuid.UUID) -> Candidate | None:
        stmt = select(Candidate).where(Candidate.id == cand_id, Candidate.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_posting(
        self, posting_id: uuid.UUID, stage: str | None = None,
        page: int = 1, page_size: int = 20,
    ) -> tuple[list[Candidate], int]:
        stmt = select(Candidate).where(
            Candidate.job_posting_id == posting_id,
            Candidate.is_deleted == False,
        )
        count_stmt = select(func.count(Candidate.id)).where(
            Candidate.job_posting_id == posting_id,
            Candidate.is_deleted == False,
        )

        if stage:
            stmt = stmt.where(Candidate.stage == stage)
            count_stmt = count_stmt.where(Candidate.stage == stage)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(Candidate.ai_score.desc().nullslast(), Candidate.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def count_by_stage(self) -> dict[str, int]:
        stmt = (
            select(Candidate.stage, func.count(Candidate.id))
            .where(Candidate.is_deleted == False)
            .group_by(Candidate.stage)
        )
        result = await self.db.execute(stmt)
        return {stage: count for stage, count in result.all()}

    async def count_by_source(self) -> list[dict]:
        stmt = (
            select(Candidate.source, func.count(Candidate.id))
            .where(Candidate.is_deleted == False)
            .group_by(Candidate.source)
            .order_by(func.count(Candidate.id).desc())
        )
        result = await self.db.execute(stmt)
        return [{"source": source, "count": count} for source, count in result.all()]

    async def total_count(self) -> int:
        stmt = select(func.count(Candidate.id)).where(Candidate.is_deleted == False)
        return (await self.db.execute(stmt)).scalar() or 0
