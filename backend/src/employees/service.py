"""
Employee module — Business logic for employee management.
"""

import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.repository import AuditLogRepository, UserRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException, ValidationException
from src.core.security import UserRole, hash_password
from src.employees.models import (
    Department, Designation, Employee, EmployeeSkill, EmployeeTimeline,
)
from src.employees.repository import (
    DepartmentRepository, DesignationRepository, EmployeeRepository,
)
from src.employees.schemas import (
    DepartmentCreateRequest, DepartmentResponse, DesignationCreateRequest,
    DesignationResponse, EmployeeCreateRequest, EmployeeDetailResponse,
    EmployeeListResponse, EmployeeUpdateRequest, SkillRequest, SkillResponse,
)


class EmployeeService:
    """Business logic for employee operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.desig_repo = DesignationRepository(db)
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditLogRepository(db)

    async def create_employee(
        self, data: EmployeeCreateRequest, created_by: uuid.UUID
    ) -> EmployeeDetailResponse:
        """Create a new employee with a linked user account."""
        # Check for duplicate employee code
        existing = await self.employee_repo.get_by_code(data.employee_code)
        if existing:
            raise AlreadyExistsException("Employee", "code", data.employee_code)

        # Check email
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise AlreadyExistsException("User", "email", data.email)

        # Create user account
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password or "Welcome@123"),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.work_phone or data.personal_phone,
            primary_role=UserRole.EMPLOYEE,
            is_active=True,
            is_verified=True,
        )
        user = await self.user_repo.create(user)

        # Create employee record
        employee = Employee(
            user_id=user.id,
            employee_code=data.employee_code,
            department_id=data.department_id,
            designation_id=data.designation_id,
            reporting_manager_id=data.reporting_manager_id,
            employment_type=data.employment_type,
            employment_status="active",
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            marital_status=data.marital_status,
            blood_group=data.blood_group,
            nationality=data.nationality,
            personal_email=data.personal_email,
            work_phone=data.work_phone,
            personal_phone=data.personal_phone,
            current_address=data.current_address,
            permanent_address=data.permanent_address,
            city=data.city,
            state=data.state,
            country=data.country,
            pin_code=data.pin_code,
            date_of_joining=data.date_of_joining,
            ctc=data.ctc,
            basic_salary=data.basic_salary,
            bank_name=data.bank_name,
            bank_account_number=data.bank_account_number,
            ifsc_code=data.ifsc_code,
            pan_number=data.pan_number,
            uan_number=data.uan_number,
            work_location=data.work_location,
        )
        employee = await self.employee_repo.create(employee)

        # Add joining timeline event
        self.db.add(EmployeeTimeline(
            employee_id=employee.id,
            event_type="joining",
            title="Joined the organization",
            event_date=data.date_of_joining,
            created_by=created_by,
        ))
        await self.db.flush()

        # Audit
        await self.audit_repo.create(
            action="employee.created",
            resource_type="employee",
            resource_id=str(employee.id),
            user_id=created_by,
            details=f"Employee {data.first_name} {data.last_name} ({data.employee_code}) created",
        )

        return await self._to_detail_response(employee)

    async def get_employee(self, employee_id: uuid.UUID) -> EmployeeDetailResponse:
        """Get a single employee by ID."""
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee", employee_id)
        return await self._to_detail_response(employee)

    async def get_employee_by_user(self, user_id: uuid.UUID) -> EmployeeDetailResponse:
        """Get employee by user ID (for self-service)."""
        employee = await self.employee_repo.get_by_user_id(user_id)
        if not employee:
            raise NotFoundException("Employee")
        return await self._to_detail_response(employee)

    async def list_employees(
        self,
        page: int = 1,
        page_size: int = 20,
        department_id: uuid.UUID | None = None,
        designation_id: uuid.UUID | None = None,
        employment_status: str | None = None,
        employment_type: str | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> dict:
        """List employees with pagination and filters."""
        employees, total = await self.employee_repo.get_all(
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

        total_pages = (total + page_size - 1) // page_size

        items = []
        for emp in employees:
            items.append(EmployeeListResponse(
                id=emp.id,
                employee_code=emp.employee_code,
                user_id=emp.user_id,
                first_name=emp.user.first_name if emp.user else "",
                last_name=emp.user.last_name if emp.user else "",
                full_name=emp.user.full_name if emp.user else "",
                email=emp.user.email if emp.user else "",
                avatar_url=emp.user.avatar_url if emp.user else None,
                department_name=emp.department.name if emp.department else None,
                designation_title=emp.designation.title if emp.designation else None,
                employment_type=emp.employment_type,
                employment_status=emp.employment_status,
                date_of_joining=emp.date_of_joining,
                work_location=emp.work_location,
                city=emp.city,
            ))

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    async def update_employee(
        self, employee_id: uuid.UUID, data: EmployeeUpdateRequest, updated_by: uuid.UUID
    ) -> EmployeeDetailResponse:
        """Update employee fields."""
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationException("No fields to update")

        employee = await self.employee_repo.update(employee_id, **update_data)
        if not employee:
            raise NotFoundException("Employee", employee_id)

        await self.audit_repo.create(
            action="employee.updated",
            resource_type="employee",
            resource_id=str(employee_id),
            user_id=updated_by,
            details=f"Fields updated: {', '.join(update_data.keys())}",
        )

        return await self._to_detail_response(employee)

    async def add_skill(
        self, employee_id: uuid.UUID, data: SkillRequest
    ) -> SkillResponse:
        """Add a skill to an employee."""
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee", employee_id)

        skill = EmployeeSkill(
            employee_id=employee_id,
            skill_name=data.skill_name,
            category=data.category,
            proficiency=data.proficiency,
            years_experience=data.years_experience,
            is_primary=data.is_primary,
        )
        self.db.add(skill)
        await self.db.flush()
        await self.db.refresh(skill)
        return SkillResponse.model_validate(skill)

    async def get_dashboard_stats(self) -> dict:
        """Get dashboard statistics."""
        total_active = await self.employee_repo.count_active()
        dept_distribution = await self.employee_repo.count_by_department()
        recent_hires = await self.employee_repo.get_recent_hires(5)
        upcoming_bdays = await self.employee_repo.get_upcoming_birthdays(5)

        recent_hire_list = []
        for emp in recent_hires:
            recent_hire_list.append({
                "name": emp.user.full_name if emp.user else "Unknown",
                "department": emp.department.name if emp.department else "N/A",
                "designation": emp.designation.title if emp.designation else "N/A",
                "date_of_joining": emp.date_of_joining.isoformat(),
            })

        bday_list = []
        for emp in upcoming_bdays:
            bday_list.append({
                "name": emp.user.full_name if emp.user else "Unknown",
                "department": emp.department.name if emp.department else "N/A",
                "date_of_birth": emp.date_of_birth.isoformat() if emp.date_of_birth else None,
            })

        return {
            "total_employees": total_active,
            "department_distribution": dept_distribution,
            "recent_hires": recent_hire_list,
            "upcoming_birthdays": bday_list,
        }

    # ── Department CRUD ──────────────────────────────────────
    async def list_departments(self) -> list[DepartmentResponse]:
        departments = await self.dept_repo.get_all()
        return [DepartmentResponse.model_validate(d) for d in departments]

    async def create_department(self, data: DepartmentCreateRequest) -> DepartmentResponse:
        dept = Department(**data.model_dump())
        dept = await self.dept_repo.create(dept)
        return DepartmentResponse.model_validate(dept)

    # ── Designation CRUD ─────────────────────────────────────
    async def list_designations(self) -> list[DesignationResponse]:
        designations = await self.desig_repo.get_all()
        return [DesignationResponse.model_validate(d) for d in designations]

    async def create_designation(self, data: DesignationCreateRequest) -> DesignationResponse:
        desig = Designation(**data.model_dump())
        desig = await self.desig_repo.create(desig)
        return DesignationResponse.model_validate(desig)

    # ── Private Helpers ──────────────────────────────────────
    async def _to_detail_response(self, employee: Employee) -> EmployeeDetailResponse:
        """Convert Employee model to detailed response."""
        # Ensure relationships are loaded
        if not employee.user:
            employee = await self.employee_repo.get_by_id(employee.id)

        manager_name = None
        if employee.reporting_manager_id:
            manager = await self.employee_repo.get_by_id(employee.reporting_manager_id)
            if manager and manager.user:
                manager_name = manager.user.full_name

        return EmployeeDetailResponse(
            id=employee.id,
            employee_code=employee.employee_code,
            user_id=employee.user_id,
            first_name=employee.user.first_name if employee.user else "",
            last_name=employee.user.last_name if employee.user else "",
            full_name=employee.user.full_name if employee.user else "",
            email=employee.user.email if employee.user else "",
            avatar_url=employee.user.avatar_url if employee.user else None,
            phone=employee.user.phone if employee.user else None,
            department=DepartmentResponse.model_validate(employee.department) if employee.department else None,
            designation=DesignationResponse.model_validate(employee.designation) if employee.designation else None,
            reporting_manager_name=manager_name,
            employment_type=employee.employment_type,
            employment_status=employee.employment_status,
            date_of_joining=employee.date_of_joining,
            date_of_confirmation=employee.date_of_confirmation,
            date_of_exit=employee.date_of_exit,
            notice_period_days=employee.notice_period_days,
            date_of_birth=employee.date_of_birth,
            gender=employee.gender,
            marital_status=employee.marital_status,
            blood_group=employee.blood_group,
            nationality=employee.nationality,
            personal_email=employee.personal_email,
            work_phone=employee.work_phone,
            personal_phone=employee.personal_phone,
            current_address=employee.current_address,
            permanent_address=employee.permanent_address,
            city=employee.city,
            state=employee.state,
            country=employee.country,
            pin_code=employee.pin_code,
            ctc=employee.ctc,
            basic_salary=employee.basic_salary,
            bank_name=employee.bank_name,
            pan_number=employee.pan_number,
            work_location=employee.work_location,
            shift=employee.shift,
            ai_summary=employee.ai_summary,
            skills=[SkillResponse.model_validate(s) for s in (employee.skills or [])],
            created_at=employee.created_at,
        )
