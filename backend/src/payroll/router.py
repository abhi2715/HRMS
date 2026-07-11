"""
Payroll module — API router.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.dependencies import PermissionChecker, get_current_user_id
from src.employees.repository import EmployeeRepository
from src.payroll.schemas import PayrollRunCreate, PayrollRunResponse, PayslipResponse, SalaryStructureResponse
from src.payroll.service import PayrollService

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.get("/dashboard", summary="Payroll dashboard",
            dependencies=[Depends(PermissionChecker("payroll:read"))])
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    service = PayrollService(db)
    return await service.get_dashboard()


@router.post("/run", response_model=PayrollRunResponse, status_code=status.HTTP_201_CREATED,
             summary="Run payroll", dependencies=[Depends(PermissionChecker("payroll:process"))])
async def run_payroll(
    data: PayrollRunCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    return await service.run_payroll(data, processed_by=user_id)


@router.get("/runs", summary="List payroll runs",
            dependencies=[Depends(PermissionChecker("payroll:read"))])
async def list_runs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    return await service.list_runs(page, page_size)


@router.get("/runs/{run_id}/payslips", summary="Get payslips for a run",
            dependencies=[Depends(PermissionChecker("payroll:read"))])
async def get_payslips(
    run_id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    return await service.get_payslips(run_id, page, page_size)


@router.get("/my-payslips", response_model=list[PayslipResponse], summary="My payslips")
async def get_my_payslips(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    emp = await EmployeeRepository(db).get_by_user_id(user_id)
    service = PayrollService(db)
    return await service.get_my_payslips(emp.id)


@router.get("/salary-structures", response_model=list[SalaryStructureResponse],
            summary="List salary structures")
async def get_structures(db: AsyncSession = Depends(get_db)):
    service = PayrollService(db)
    return await service.get_salary_structures()
