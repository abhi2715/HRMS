"""
Leave management — SQLAlchemy models.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import BaseModel


class LeaveType(BaseModel):
    """Types of leave (Casual, Sick, Privilege, etc.)."""

    __tablename__ = "leave_types"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    max_days_per_year: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_carry_forward: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    max_carry_forward_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_encashable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    min_days_notice: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    applies_after_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Probation
    sandwich_policy: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)

    balances = relationship("LeaveBalance", back_populates="leave_type", lazy="noload")


class LeaveBalance(BaseModel):
    """Employee leave balance for a specific type and year."""

    __tablename__ = "leave_balances"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    leave_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leave_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    allocated: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=False, default=0)
    used: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=False, default=0)
    carried_forward: Mapped[Decimal] = mapped_column(Numeric(5, 1), nullable=False, default=0)

    @property
    def available(self) -> Decimal:
        return self.allocated + self.carried_forward - self.used

    employee = relationship("Employee", back_populates="leave_balances")
    leave_type = relationship("LeaveType", back_populates="balances", lazy="selectin")


class LeaveRequest(BaseModel):
    """Employee leave request."""

    __tablename__ = "leave_requests"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    leave_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leave_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_days: Mapped[Decimal] = mapped_column(Numeric(4, 1), nullable=False)
    is_half_day: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    half_day_type: Mapped[str | None] = mapped_column(String(20), nullable=True)  # first_half, second_half
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", index=True,
    )  # pending, approved, rejected, cancelled, escalated
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    employee = relationship("Employee", back_populates="leave_requests")
    leave_type = relationship("LeaveType", lazy="selectin")


class Holiday(BaseModel):
    """Public holidays and company holidays."""

    __tablename__ = "holidays"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(30), nullable=False, default="public")  # public, restricted, company
    is_optional: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
