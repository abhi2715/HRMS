"""
Payroll module — SQLAlchemy models.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import BaseModel


class SalaryStructure(BaseModel):
    """Salary component structure (Basic, HRA, DA, etc.)."""

    __tablename__ = "salary_structures"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    components: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # Example: {"basic": 40, "hra": 20, "da": 10, "special_allowance": 30} (percentages of CTC)

    payslips = relationship("Payslip", back_populates="salary_structure", lazy="noload")


class PayrollRun(BaseModel):
    """Monthly payroll processing run."""

    __tablename__ = "payroll_runs"

    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="draft", nullable=False, index=True,
    )  # draft, processing, completed, approved, paid
    total_employees: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_gross: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    total_deductions: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    total_net: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    processed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_anomalies: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    payslips = relationship("Payslip", back_populates="payroll_run", lazy="noload")


class Payslip(BaseModel):
    """Individual employee payslip for a payroll run."""

    __tablename__ = "payslips"

    payroll_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("payroll_runs.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    salary_structure_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("salary_structures.id", ondelete="SET NULL"),
        nullable=True,
    )
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # ── Earnings ─────────────────────────────────────────────
    basic: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    hra: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    da: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    special_allowance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    bonus: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    overtime_pay: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    other_earnings: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    gross_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    # ── Deductions ───────────────────────────────────────────
    pf_employee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)  # 12% of basic
    pf_employer: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    esi_employee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    esi_employer: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    professional_tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    income_tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    other_deductions: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    total_deductions: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    # ── Net ──────────────────────────────────────────────────
    net_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    # ── Working Days ─────────────────────────────────────────
    total_working_days: Mapped[int] = mapped_column(Integer, default=22, nullable=False)
    days_worked: Mapped[int] = mapped_column(Integer, default=22, nullable=False)
    lop_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Loss of Pay

    # ── Status ───────────────────────────────────────────────
    status: Mapped[str] = mapped_column(String(20), default="generated", nullable=False)
    payment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ── JSON breakdown ───────────────────────────────────────
    earnings_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    deductions_breakdown: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    payroll_run = relationship("PayrollRun", back_populates="payslips")
    salary_structure = relationship("SalaryStructure", back_populates="payslips", lazy="selectin")
    employee = relationship("Employee", lazy="selectin")


class TaxDeclaration(BaseModel):
    """Employee annual tax declaration for TDS calculation."""

    __tablename__ = "tax_declarations"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    financial_year: Mapped[str] = mapped_column(String(10), nullable=False)  # 2024-25
    regime: Mapped[str] = mapped_column(String(10), default="new", nullable=False)  # old, new
    declarations: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    total_declared: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    verified_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
