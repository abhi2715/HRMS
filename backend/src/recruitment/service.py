"""
Recruitment module — Business logic.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.employees.repository import DepartmentRepository
from src.recruitment.models import Candidate, JobPosting
from src.recruitment.repository import CandidateRepository, JobPostingRepository
from src.recruitment.schemas import (
    CandidateCreateRequest, CandidateResponse, CandidateStageUpdate,
    JobPostingCreateRequest, JobPostingResponse, RecruitmentDashboard,
)


class RecruitmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.posting_repo = JobPostingRepository(db)
        self.candidate_repo = CandidateRepository(db)
        self.dept_repo = DepartmentRepository(db)

    async def create_posting(self, data: JobPostingCreateRequest) -> JobPostingResponse:
        posting = JobPosting(
            title=data.title,
            department_id=data.department_id,
            description=data.description,
            requirements=data.requirements,
            required_skills=data.required_skills,
            experience_min=data.experience_min,
            experience_max=data.experience_max,
            salary_min=data.salary_min,
            salary_max=data.salary_max,
            location=data.location,
            job_type=data.job_type,
            positions=data.positions,
            status="open",
            posted_at=datetime.now(timezone.utc),
        )
        posting = await self.posting_repo.create(posting)
        return await self._posting_response(posting)

    async def list_postings(
        self, status: str | None = None, page: int = 1, page_size: int = 20,
    ) -> dict:
        postings, total = await self.posting_repo.get_all(status=status, page=page, page_size=page_size)
        items = []
        for p in postings:
            items.append(await self._posting_response(p))
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_posting(self, posting_id: uuid.UUID) -> JobPostingResponse:
        posting = await self.posting_repo.get_by_id(posting_id)
        if not posting:
            raise NotFoundException("Job Posting", posting_id)
        return await self._posting_response(posting)

    async def add_candidate(self, data: CandidateCreateRequest) -> CandidateResponse:
        posting = await self.posting_repo.get_by_id(data.job_posting_id)
        if not posting:
            raise NotFoundException("Job Posting", data.job_posting_id)

        candidate = Candidate(
            job_posting_id=data.job_posting_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            experience_years=data.experience_years,
            current_ctc=data.current_ctc,
            expected_ctc=data.expected_ctc,
            notice_period_days=data.notice_period_days,
            source=data.source,
            stage="applied",
            skills_extracted=data.skills_extracted,
        )
        candidate = await self.candidate_repo.create(candidate)
        return self._candidate_response(candidate, job_title=posting.title)

    async def get_candidates(
        self, posting_id: uuid.UUID, stage: str | None = None,
        page: int = 1, page_size: int = 20,
    ) -> dict:
        candidates, total = await self.candidate_repo.get_by_posting(
            posting_id, stage=stage, page=page, page_size=page_size,
        )
        posting = await self.posting_repo.get_by_id(posting_id)
        items = [self._candidate_response(c, job_title=posting.title if posting else None) for c in candidates]
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def update_candidate_stage(
        self, candidate_id: uuid.UUID, data: CandidateStageUpdate,
    ) -> CandidateResponse:
        candidate = await self.candidate_repo.get_by_id(candidate_id)
        if not candidate:
            raise NotFoundException("Candidate", candidate_id)

        candidate.stage = data.stage
        await self.db.flush()
        await self.db.refresh(candidate)

        posting = await self.posting_repo.get_by_id(candidate.job_posting_id)
        return self._candidate_response(candidate, job_title=posting.title if posting else None)

    async def get_dashboard(self) -> RecruitmentDashboard:
        open_positions = await self.posting_repo.count_open()
        total_applicants = await self.candidate_repo.total_count()
        stage_counts = await self.candidate_repo.count_by_stage()
        top_sources = await self.candidate_repo.count_by_source()

        return RecruitmentDashboard(
            total_open_positions=open_positions,
            total_applicants=total_applicants,
            shortlisted=stage_counts.get("shortlisted", 0),
            interviews_scheduled=stage_counts.get("interview", 0) + stage_counts.get("technical", 0),
            offers_sent=stage_counts.get("offer", 0),
            pipeline_by_stage=stage_counts,
            top_sources=top_sources[:5],
        )

    async def _posting_response(self, posting: JobPosting) -> JobPostingResponse:
        dept_name = None
        if posting.department_id:
            dept = await self.dept_repo.get_by_id(posting.department_id)
            if dept:
                dept_name = dept.name

        _, total_applicants = await self.candidate_repo.get_by_posting(posting.id, page_size=0)

        return JobPostingResponse(
            id=posting.id,
            title=posting.title,
            department_name=dept_name,
            description=posting.description,
            requirements=posting.requirements,
            required_skills=posting.required_skills,
            experience_min=posting.experience_min,
            experience_max=posting.experience_max,
            salary_min=posting.salary_min,
            salary_max=posting.salary_max,
            location=posting.location,
            job_type=posting.job_type,
            positions=posting.positions,
            status=posting.status,
            total_applicants=total_applicants,
            posted_at=posting.posted_at,
            created_at=posting.created_at,
        )

    def _candidate_response(self, c: Candidate, job_title: str | None = None) -> CandidateResponse:
        return CandidateResponse(
            id=c.id,
            job_posting_id=c.job_posting_id,
            job_title=job_title,
            first_name=c.first_name,
            last_name=c.last_name,
            full_name=f"{c.first_name} {c.last_name}",
            email=c.email,
            phone=c.phone,
            experience_years=c.experience_years,
            current_ctc=c.current_ctc,
            expected_ctc=c.expected_ctc,
            notice_period_days=c.notice_period_days,
            source=c.source,
            stage=c.stage,
            ai_score=c.ai_score,
            ai_evaluation=c.ai_evaluation,
            skills_extracted=c.skills_extracted,
            created_at=c.created_at,
        )
