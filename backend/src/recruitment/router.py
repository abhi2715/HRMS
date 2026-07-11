"""
Recruitment module — API router.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.recruitment.schemas import (
    CandidateCreateRequest, CandidateResponse, CandidateStageUpdate,
    JobPostingCreateRequest, JobPostingResponse, RecruitmentDashboard,
)
from src.recruitment.service import RecruitmentService

router = APIRouter(prefix="/recruitment", tags=["Recruitment"])


@router.get(
    "/dashboard",
    response_model=RecruitmentDashboard,
    summary="Recruitment dashboard",
    dependencies=[Depends(PermissionChecker("recruitment:read"))],
)
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    service = RecruitmentService(db)
    return await service.get_dashboard()


@router.get(
    "/postings",
    summary="List job postings",
    dependencies=[Depends(PermissionChecker("recruitment:read"))],
)
async def list_postings(
    status_filter: str | None = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = RecruitmentService(db)
    return await service.list_postings(status=status_filter, page=page, page_size=page_size)


@router.post(
    "/postings",
    response_model=JobPostingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create job posting",
    dependencies=[Depends(PermissionChecker("recruitment:write"))],
)
async def create_posting(
    data: JobPostingCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    service = RecruitmentService(db)
    return await service.create_posting(data)


@router.get(
    "/postings/{posting_id}",
    response_model=JobPostingResponse,
    summary="Get job posting",
    dependencies=[Depends(PermissionChecker("recruitment:read"))],
)
async def get_posting(
    posting_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = RecruitmentService(db)
    return await service.get_posting(posting_id)


@router.get(
    "/postings/{posting_id}/candidates",
    summary="List candidates for a posting",
    dependencies=[Depends(PermissionChecker("recruitment:read"))],
)
async def list_candidates(
    posting_id: uuid.UUID,
    stage: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = RecruitmentService(db)
    return await service.get_candidates(posting_id, stage=stage, page=page, page_size=page_size)


@router.post(
    "/candidates",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add candidate",
    dependencies=[Depends(PermissionChecker("recruitment:write"))],
)
async def add_candidate(
    data: CandidateCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    service = RecruitmentService(db)
    return await service.add_candidate(data)


@router.patch(
    "/candidates/{candidate_id}/stage",
    response_model=CandidateResponse,
    summary="Update candidate stage",
    dependencies=[Depends(PermissionChecker("recruitment:write"))],
)
async def update_stage(
    candidate_id: uuid.UUID,
    data: CandidateStageUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = RecruitmentService(db)
    return await service.update_candidate_stage(candidate_id, data)
