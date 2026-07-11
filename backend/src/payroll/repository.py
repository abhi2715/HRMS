"""
Payroll module — Repository layer.
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.payroll.models import PayrollRun, Payslip, SalaryStructure


class PayrollRunRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, run: PayrollRun) -> PayrollRun:
        self.db.add(run)
        await self.db.flush()
        await self.db.refresh(run)
        return run

    async def get_by_id(self, run_id: uuid.UUID) -> PayrollRun | None:
        stmt = select(PayrollRun).where(PayrollRun.id == run_id, PayrollRun.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[PayrollRun], int]:
        stmt = (
            select(PayrollRun)
            .where(PayrollRun.is_deleted == False)
            .order_by(PayrollRun.year.desc(), PayrollRun.month.desc())
        )
        count_stmt = select(func.count(PayrollRun.id)).where(PayrollRun.is_deleted == False)
        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def get_latest(self) -> PayrollRun | None:
        stmt = (
            select(PayrollRun)
            .where(PayrollRun.is_deleted == False)
            .order_by(PayrollRun.year.desc(), PayrollRun.month.desc())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class PayslipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_bulk(self, payslips: list[Payslip]) -> list[Payslip]:
        self.db.add_all(payslips)
        await self.db.flush()
        return payslips

    async def get_by_run(self, run_id: uuid.UUID, page: int = 1, page_size: int = 50) -> tuple[list[Payslip], int]:
        stmt = (
            select(Payslip)
            .where(Payslip.payroll_run_id == run_id, Payslip.is_deleted == False)
            .order_by(Payslip.net_salary.desc())
        )
        count_stmt = select(func.count(Payslip.id)).where(
            Payslip.payroll_run_id == run_id, Payslip.is_deleted == False
        )
        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def get_by_employee(self, employee_id: uuid.UUID, limit: int = 12) -> list[Payslip]:
        stmt = (
            select(Payslip)
            .where(Payslip.employee_id == employee_id, Payslip.is_deleted == False)
            .order_by(Payslip.year.desc(), Payslip.month.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_total_payroll(self) -> dict:
        stmt = (
            select(
                func.sum(Payslip.gross_salary),
                func.sum(Payslip.total_deductions),
                func.sum(Payslip.net_salary),
                func.count(Payslip.id),
            )
            .where(Payslip.is_deleted == False)
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()
        if row:
            return {
                "total_gross": row[0] or 0,
                "total_deductions": row[1] or 0,
                "total_net": row[2] or 0,
                "total_payslips": row[3] or 0,
            }
        return {"total_gross": 0, "total_deductions": 0, "total_net": 0, "total_payslips": 0}


class SalaryStructureRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[SalaryStructure]:
        stmt = select(SalaryStructure).where(SalaryStructure.is_deleted == False).order_by(SalaryStructure.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_active(self) -> SalaryStructure | None:
        stmt = select(SalaryStructure).where(
            SalaryStructure.is_active == True, SalaryStructure.is_deleted == False
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
