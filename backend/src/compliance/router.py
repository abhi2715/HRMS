"""
Compliance module — Schemas & API router.
"""

import uuid
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.compliance.models import CompliancePolicy, PolicyAcknowledgment
from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.core.exceptions import NotFoundException
from src.employees.repository import EmployeeRepository


# ── Schemas ──────────────────────────────────────────────────

class PolicyResponse(BaseModel):
    id: uuid.UUID
    title: str
    category: str
    description: str | None
    content: str | None
    version: str
    effective_date: date
    is_mandatory: bool
    is_active: bool
    acknowledgment_count: int = 0
    model_config = {"from_attributes": True}


class AcknowledgmentResponse(BaseModel):
    id: uuid.UUID
    policy_id: uuid.UUID
    policy_title: str | None = None
    employee_id: uuid.UUID
    acknowledged_at: datetime
    model_config = {"from_attributes": True}





class AcknowledgeRequest(BaseModel):
    policy_id: uuid.UUID


# ── Router ───────────────────────────────────────────────────

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/policies", response_model=list[PolicyResponse], summary="List policies")
async def list_policies(
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CompliancePolicy).where(CompliancePolicy.is_deleted == False, CompliancePolicy.is_active == True)
    if category:
        stmt = stmt.where(CompliancePolicy.category == category)
    stmt = stmt.order_by(CompliancePolicy.title)
    result = await db.execute(stmt)
    policies = list(result.scalars().all())
    return [PolicyResponse.model_validate(p) for p in policies]


@router.get("/policies/{policy_id}", response_model=PolicyResponse, summary="Get policy")
async def get_policy(policy_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    policy = await db.get(CompliancePolicy, policy_id)
    if not policy or policy.is_deleted:
        raise NotFoundException("Policy", policy_id)
    return PolicyResponse.model_validate(policy)


@router.post("/acknowledge", response_model=AcknowledgmentResponse,
             status_code=status.HTTP_201_CREATED, summary="Acknowledge policy")
async def acknowledge_policy(
    data: AcknowledgeRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    policy = await db.get(CompliancePolicy, data.policy_id)
    if not policy:
        raise NotFoundException("Policy", data.policy_id)

    ack = PolicyAcknowledgment(
        policy_id=data.policy_id,
        employee_id=emp.id,
    )
    db.add(ack)
    await db.flush()
    await db.refresh(ack)

    return AcknowledgmentResponse(
        id=ack.id, policy_id=ack.policy_id,
        policy_title=policy.title, employee_id=ack.employee_id,
        acknowledged_at=ack.acknowledged_at,
    )


@router.get("/my-acknowledgments", response_model=list[AcknowledgmentResponse], summary="My acknowledgments")
async def my_acknowledgments(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    stmt = (
        select(PolicyAcknowledgment)
        .where(PolicyAcknowledgment.employee_id == emp.id, PolicyAcknowledgment.is_deleted == False)
        .order_by(PolicyAcknowledgment.acknowledged_at.desc())
    )
    result = await db.execute(stmt)
    acks = list(result.scalars().all())
    items = []
    for a in acks:
        policy = await db.get(CompliancePolicy, a.policy_id)
        items.append(AcknowledgmentResponse(
            id=a.id, policy_id=a.policy_id,
            policy_title=policy.title if policy else None,
            employee_id=a.employee_id, acknowledged_at=a.acknowledged_at,
        ))
    return items





@router.get("/dashboard", summary="Compliance dashboard",
            dependencies=[Depends(PermissionChecker("compliance:read"))])
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    total_policies = (await db.execute(
        select(func.count(CompliancePolicy.id)).where(CompliancePolicy.is_deleted == False, CompliancePolicy.is_active == True)
    )).scalar() or 0

    total_acks = (await db.execute(
        select(func.count(PolicyAcknowledgment.id)).where(PolicyAcknowledgment.is_deleted == False)
    )).scalar() or 0

    return {
        "total_policies": total_policies,
        "total_acknowledgments": total_acks,
        "open_violations": 0,
        "resolved_violations": 0,
    }
