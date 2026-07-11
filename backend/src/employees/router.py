"""
Employee module — API router with all employee endpoints.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.dependencies import (
    PermissionChecker,
    get_current_user_id,
)
from src.employees.schemas import (
    DepartmentCreateRequest,
    DepartmentResponse,
    DesignationCreateRequest,
    DesignationResponse,
    EmployeeCreateRequest,
    EmployeeDetailResponse,
    EmployeeUpdateRequest,
    SkillRequest,
    SkillResponse,
)
from src.employees.service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


# ── Employee CRUD ────────────────────────────────────────────

@router.get(
    "",
    summary="List all employees",
    dependencies=[Depends(PermissionChecker("employees:read"))],
)
async def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    department_id: uuid.UUID | None = Query(None),
    designation_id: uuid.UUID | None = Query(None),
    employment_status: str | None = Query(None),
    employment_type: str | None = Query(None),
    search: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: AsyncSession = Depends(get_db),
):
    """List employees with pagination, filtering, sorting, and search."""
    service = EmployeeService(db)
    return await service.list_employees(
        page=page,
        page_size=page_size,
        department_id=department_id,
        designation_id=designation_id,
        employment_status=employment_status,
        employment_type=employment_type,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.post(
    "",
    response_model=EmployeeDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    dependencies=[Depends(PermissionChecker("employees:write"))],
)
async def create_employee(
    data: EmployeeCreateRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new employee with a linked user account."""
    service = EmployeeService(db)
    return await service.create_employee(data, created_by=user_id)


@router.get(
    "/me",
    response_model=EmployeeDetailResponse,
    summary="Get my employee profile",
)
async def get_my_profile(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's employee profile."""
    service = EmployeeService(db)
    return await service.get_employee_by_user(user_id)


@router.get(
    "/dashboard-stats",
    summary="Get dashboard statistics",
    dependencies=[Depends(PermissionChecker("employees:read"))],
)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated dashboard statistics."""
    service = EmployeeService(db)
    return await service.get_dashboard_stats()


@router.get(
    "/{employee_id}",
    response_model=EmployeeDetailResponse,
    summary="Get employee by ID",
    dependencies=[Depends(PermissionChecker("employees:read"))],
)
async def get_employee(
    employee_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a single employee's full profile."""
    service = EmployeeService(db)
    return await service.get_employee(employee_id)


@router.patch(
    "/{employee_id}",
    response_model=EmployeeDetailResponse,
    summary="Update employee",
    dependencies=[Depends(PermissionChecker("employees:write"))],
)
async def update_employee(
    employee_id: uuid.UUID,
    data: EmployeeUpdateRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update employee fields."""
    service = EmployeeService(db)
    return await service.update_employee(employee_id, data, updated_by=user_id)


@router.post(
    "/{employee_id}/skills",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add skill to employee",
    dependencies=[Depends(PermissionChecker("employees:write"))],
)
async def add_skill(
    employee_id: uuid.UUID,
    data: SkillRequest,
    db: AsyncSession = Depends(get_db),
):
    """Add a skill to an employee's profile."""
    service = EmployeeService(db)
    return await service.add_skill(employee_id, data)


# ── Department Endpoints ─────────────────────────────────────

@router.get(
    "/departments/all",
    response_model=list[DepartmentResponse],
    summary="List all departments",
)
async def list_departments(
    db: AsyncSession = Depends(get_db),
):
    """List all active departments."""
    service = EmployeeService(db)
    return await service.list_departments()


@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create department",
    dependencies=[Depends(PermissionChecker("departments:write"))],
)
async def create_department(
    data: DepartmentCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new department."""
    service = EmployeeService(db)
    return await service.create_department(data)


# ── Designation Endpoints ────────────────────────────────────

@router.get(
    "/designations/all",
    response_model=list[DesignationResponse],
    summary="List all designations",
)
async def list_designations(
    db: AsyncSession = Depends(get_db),
):
    """List all active designations."""
    service = EmployeeService(db)
    return await service.list_designations()


@router.post(
    "/designations",
    response_model=DesignationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create designation",
    dependencies=[Depends(PermissionChecker("designations:write"))],
)
async def create_designation(
    data: DesignationCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new designation."""
    service = EmployeeService(db)
    return await service.create_designation(data)
