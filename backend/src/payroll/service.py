"""
Payroll module — Business logic.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException, ValidationException
from src.employees.repository import EmployeeRepository
from src.payroll.models import PayrollRun, Payslip
from src.payroll.repository import PayrollRunRepository, PayslipRepository, SalaryStructureRepository
from src.payroll.schemas import PayrollRunCreate, PayrollRunResponse, PayslipResponse, SalaryStructureResponse


class PayrollService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.run_repo = PayrollRunRepository(db)
        self.payslip_repo = PayslipRepository(db)
        self.structure_repo = SalaryStructureRepository(db)
        self.employee_repo = EmployeeRepository(db)

    async def run_payroll(self, data: PayrollRunCreate, processed_by: uuid.UUID) -> PayrollRunResponse:
        """Process payroll for all active employees."""
        # Get all active employees
        employees, total = await self.employee_repo.get_all(
            page=1, page_size=500, employment_status="active"
        )
        if not employees:
            raise ValidationException("No active employees found")

        structure = await self.structure_repo.get_active()
        basic_pct = Decimal(str(structure.basic_pct)) if structure else Decimal("0.40")
        hra_pct = Decimal(str(structure.hra_pct)) if structure else Decimal("0.20")
        special_pct = Decimal(str(structure.special_pct)) if structure else Decimal("0.23")
        da_pct = Decimal(str(structure.da_pct)) if structure else Decimal("0.05")
        pf_pct = Decimal(str(structure.pf_pct)) if structure else Decimal("0.12")

        payslips = []
        total_gross = Decimal(0)
        total_deductions = Decimal(0)
        total_net = Decimal(0)

        for emp in employees:
            ctc = emp.ctc or Decimal(0)
            monthly_ctc = ctc / 12

            basic = monthly_ctc * basic_pct
            hra = monthly_ctc * hra_pct
            special = monthly_ctc * special_pct
            da = monthly_ctc * da_pct
            gross = basic + hra + special + da

            pf_employee = basic * pf_pct
            pf_employer = basic * pf_pct
            pt = Decimal("200") if gross > Decimal("15000") else Decimal("0")
            income_tax = gross * Decimal("0.10") if gross > Decimal("50000") else Decimal(0)
            deductions = pf_employee + pt + income_tax
            net = gross - deductions

            total_gross += gross
            total_deductions += deductions
            total_net += net

            payslips.append(Payslip(
                employee_id=emp.id,
                month=data.month,
                year=data.year,
                basic_salary=basic,
                hra=hra,
                special_allowance=special,
                dearness_allowance=da,
                gross_salary=gross,
                pf_employee=pf_employee,
                pf_employer=pf_employer,
                professional_tax=pt,
                income_tax=income_tax,
                total_deductions=deductions,
                net_salary=net,
                status="processed",
            ))

        # Create payroll run
        run = PayrollRun(
            month=data.month,
            year=data.year,
            status="completed",
            total_employees=len(employees),
            total_gross=total_gross,
            total_deductions=total_deductions,
            total_net=total_net,
            processed_by=processed_by,
            processed_at=datetime.now(timezone.utc),
        )
        run = await self.run_repo.create(run)

        # Link payslips to run
        for ps in payslips:
            ps.payroll_run_id = run.id
        await self.payslip_repo.create_bulk(payslips)

        return PayrollRunResponse(
            id=run.id, month=run.month, year=run.year, status=run.status,
            total_employees=run.total_employees, total_gross=run.total_gross,
            total_deductions=run.total_deductions, total_net=run.total_net,
            processed_at=run.processed_at, created_at=run.created_at,
        )

    async def list_runs(self, page: int = 1, page_size: int = 20) -> dict:
        runs, total = await self.run_repo.get_all(page, page_size)
        items = [PayrollRunResponse(
            id=r.id, month=r.month, year=r.year, status=r.status,
            total_employees=r.total_employees, total_gross=r.total_gross,
            total_deductions=r.total_deductions, total_net=r.total_net,
            processed_at=r.processed_at, created_at=r.created_at,
        ) for r in runs]
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_payslips(self, run_id: uuid.UUID, page: int = 1, page_size: int = 50) -> dict:
        payslips, total = await self.payslip_repo.get_by_run(run_id, page, page_size)
        items = []
        for ps in payslips:
            emp = await self.employee_repo.get_by_id(ps.employee_id)
            name = emp.user.full_name if emp and emp.user else "Unknown"
            code = emp.employee_code if emp else ""
            items.append(PayslipResponse(
                id=ps.id, payroll_run_id=ps.payroll_run_id, employee_id=ps.employee_id,
                employee_name=name, employee_code=code, month=ps.month, year=ps.year,
                basic_salary=ps.basic_salary, hra=ps.hra, special_allowance=ps.special_allowance,
                dearness_allowance=ps.dearness_allowance, gross_salary=ps.gross_salary,
                pf_employee=ps.pf_employee, pf_employer=ps.pf_employer,
                professional_tax=ps.professional_tax, income_tax=ps.income_tax,
                total_deductions=ps.total_deductions, net_salary=ps.net_salary, status=ps.status,
            ))
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_my_payslips(self, employee_id: uuid.UUID) -> list[PayslipResponse]:
        payslips = await self.payslip_repo.get_by_employee(employee_id)
        return [PayslipResponse(
            id=ps.id, payroll_run_id=ps.payroll_run_id, employee_id=ps.employee_id,
            month=ps.month, year=ps.year, basic_salary=ps.basic_salary, hra=ps.hra,
            special_allowance=ps.special_allowance, dearness_allowance=ps.dearness_allowance,
            gross_salary=ps.gross_salary, pf_employee=ps.pf_employee, pf_employer=ps.pf_employer,
            professional_tax=ps.professional_tax, income_tax=ps.income_tax,
            total_deductions=ps.total_deductions, net_salary=ps.net_salary, status=ps.status,
        ) for ps in payslips]

    async def get_salary_structures(self) -> list[SalaryStructureResponse]:
        structures = await self.structure_repo.get_all()
        return [SalaryStructureResponse.model_validate(s) for s in structures]

    async def get_dashboard(self) -> dict:
        totals = await self.payslip_repo.get_total_payroll()
        latest = await self.run_repo.get_latest()
        return {
            **totals,
            "latest_run": PayrollRunResponse(
                id=latest.id, month=latest.month, year=latest.year, status=latest.status,
                total_employees=latest.total_employees, total_gross=latest.total_gross,
                total_deductions=latest.total_deductions, total_net=latest.total_net,
                processed_at=latest.processed_at, created_at=latest.created_at,
            ) if latest else None,
        }
