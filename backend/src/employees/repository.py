"""
Employee module — Repository layer.
"""

import uuid

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.employees.models import (
    Department, Designation, Employee, EmployeeDocument,
    EmployeeSkill, EmergencyContact, EmployeeTimeline,
)


class EmployeeRepository:
    """Data access layer for Employee entities."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        await self.db.flush()
        await self.db.refresh(employee)
        return employee

    async def get_by_id(self, employee_id: uuid.UUID) -> Employee | None:
        stmt = (
            select(Employee)
            .options(
                selectinload(Employee.user),
                selectinload(Employee.department),
                selectinload(Employee.designation),
                selectinload(Employee.skills),
            )
            .where(Employee.id == employee_id, Employee.is_deleted == False)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: uuid.UUID) -> Employee | None:
        stmt = (
            select(Employee)
            .options(
                selectinload(Employee.user),
                selectinload(Employee.department),
                selectinload(Employee.designation),
                selectinload(Employee.skills),
            )
            .where(Employee.user_id == user_id, Employee.is_deleted == False)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Employee | None:
        stmt = select(Employee).where(Employee.employee_code == code, Employee.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
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
    ) -> tuple[list[Employee], int]:
        stmt = (
            select(Employee)
            .options(
                selectinload(Employee.user),
                selectinload(Employee.department),
                selectinload(Employee.designation),
                selectinload(Employee.skills),
            )
            .where(Employee.is_deleted == False)
        )
        count_stmt = select(func.count(Employee.id)).where(Employee.is_deleted == False)

        if department_id:
            stmt = stmt.where(Employee.department_id == department_id)
            count_stmt = count_stmt.where(Employee.department_id == department_id)

        if designation_id:
            stmt = stmt.where(Employee.designation_id == designation_id)
            count_stmt = count_stmt.where(Employee.designation_id == designation_id)

        if employment_status:
            stmt = stmt.where(Employee.employment_status == employment_status)
            count_stmt = count_stmt.where(Employee.employment_status == employment_status)

        if employment_type:
            stmt = stmt.where(Employee.employment_type == employment_type)
            count_stmt = count_stmt.where(Employee.employment_type == employment_type)

        if search:
            from src.auth.models import User
            stmt = stmt.join(User, Employee.user_id == User.id).where(
                User.first_name.ilike(f"%{search}%")
                | User.last_name.ilike(f"%{search}%")
                | User.email.ilike(f"%{search}%")
                | Employee.employee_code.ilike(f"%{search}%")
            )
            count_stmt = count_stmt.join(User, Employee.user_id == User.id).where(
                User.first_name.ilike(f"%{search}%")
                | User.last_name.ilike(f"%{search}%")
                | User.email.ilike(f"%{search}%")
                | Employee.employee_code.ilike(f"%{search}%")
            )

        # Count
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0

        # Sort
        sort_column = getattr(Employee, sort_by, Employee.created_at)
        if sort_order == "asc":
            stmt = stmt.order_by(sort_column.asc())
        else:
            stmt = stmt.order_by(sort_column.desc())

        # Paginate
        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        employees = list(result.scalars().all())

        return employees, total

    async def update(self, employee_id: uuid.UUID, **kwargs) -> Employee | None:
        employee = await self.get_by_id(employee_id)
        if not employee:
            return None
        for key, value in kwargs.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)
        await self.db.flush()
        await self.db.refresh(employee)
        return employee

    async def count_active(self) -> int:
        stmt = select(func.count(Employee.id)).where(
            Employee.is_deleted == False,
            Employee.employment_status == "active",
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_by_department(self) -> list[dict]:
        stmt = (
            select(Department.name, Department.color, func.count(Employee.id))
            .join(Employee, Employee.department_id == Department.id)
            .where(Employee.is_deleted == False, Employee.employment_status == "active")
            .group_by(Department.name, Department.color)
            .order_by(func.count(Employee.id).desc())
        )
        result = await self.db.execute(stmt)
        return [
            {"name": name, "color": color, "count": count}
            for name, color, count in result.all()
        ]

    async def get_recent_hires(self, limit: int = 5) -> list[Employee]:
        stmt = (
            select(Employee)
            .options(selectinload(Employee.user), selectinload(Employee.department), selectinload(Employee.designation))
            .where(Employee.is_deleted == False)
            .order_by(Employee.date_of_joining.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_upcoming_birthdays(self, limit: int = 5) -> list[Employee]:
        from datetime import date
        today = date.today()
        stmt = (
            select(Employee)
            .options(selectinload(Employee.user), selectinload(Employee.department))
            .where(
                Employee.is_deleted == False,
                Employee.date_of_birth.isnot(None),
                func.extract("month", Employee.date_of_birth) == today.month,
                func.extract("day", Employee.date_of_birth) >= today.day,
            )
            .order_by(func.extract("day", Employee.date_of_birth))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Department]:
        stmt = select(Department).where(Department.is_deleted == False).order_by(Department.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, dept_id: uuid.UUID) -> Department | None:
        stmt = select(Department).where(Department.id == dept_id, Department.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, department: Department) -> Department:
        self.db.add(department)
        await self.db.flush()
        await self.db.refresh(department)
        return department


class DesignationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Designation]:
        stmt = select(Designation).where(Designation.is_deleted == False).order_by(Designation.level, Designation.title)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, desig_id: uuid.UUID) -> Designation | None:
        stmt = select(Designation).where(Designation.id == desig_id, Designation.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, designation: Designation) -> Designation:
        self.db.add(designation)
        await self.db.flush()
        await self.db.refresh(designation)
        return designation
