"""
Attendance module — SQLAlchemy models.
"""

import uuid
from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import BaseModel


class Shift(BaseModel):
    """Work shift definition."""

    __tablename__ = "shifts"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    grace_period_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    half_day_hours: Mapped[Decimal] = mapped_column(Numeric(4, 1), default=4, nullable=False)
    full_day_hours: Mapped[Decimal] = mapped_column(Numeric(4, 1), default=8, nullable=False)
    is_night_shift: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)

    assignments = relationship("ShiftAssignment", back_populates="shift", lazy="noload")


class ShiftAssignment(BaseModel):
    """Employee-to-shift assignment."""

    __tablename__ = "shift_assignments"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    shift_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("shifts.id", ondelete="CASCADE"),
        nullable=False,
    )
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    shift = relationship("Shift", back_populates="assignments", lazy="selectin")


class AttendanceRecord(BaseModel):
    """Daily attendance record for an employee."""

    __tablename__ = "attendance_records"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    check_in: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    check_out: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="present",
    )  # present, absent, half_day, on_leave, holiday, weekend, late, remote
    work_hours: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    overtime_hours: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, default=0)
    is_late: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    late_minutes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_remote: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    check_in_latitude: Mapped[str | None] = mapped_column(String(20), nullable=True)
    check_in_longitude: Mapped[str | None] = mapped_column(String(20), nullable=True)
    check_out_latitude: Mapped[str | None] = mapped_column(String(20), nullable=True)
    check_out_longitude: Mapped[str | None] = mapped_column(String(20), nullable=True)
    device_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_anomaly_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ai_anomaly_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    employee = relationship("Employee", lazy="selectin")
