"""
Employee module — SQLAlchemy models for employees, departments, designations,
documents, skills, emergency contacts, and timeline events.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy.orm as sa_orm

from src.core.base_model import BaseModel


class Department(BaseModel):
    """Organizational department."""

    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    head_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL", use_alter=True),
        nullable=True,
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)  # Hex color for UI

    # Relationships
    employees = relationship("Employee", back_populates="department", foreign_keys="Employee.department_id", lazy="noload")
    head = relationship("Employee", foreign_keys=[head_id], lazy="selectin", post_update=True)
    children = relationship("Department", back_populates="parent", lazy="noload")
    parent = relationship("Department", remote_side="Department.id", back_populates="children", lazy="selectin")


class Designation(BaseModel):
    """Job title / designation."""

    __tablename__ = "designations"

    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # 1=Entry, 10=CXO
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    employees = relationship("Employee", back_populates="designation", lazy="noload")


class Employee(BaseModel):
    """Core employee entity linking to a user account."""

    __tablename__ = "employees"

    # ── User Link ────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False, index=True,
    )

    # ── Employment Details ───────────────────────────────────
    employee_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True,
    )
    designation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("designations.id", ondelete="SET NULL"), nullable=True,
    )
    reporting_manager_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True,
    )
    employment_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="full_time",
    )  # full_time, part_time, contract, intern
    employment_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active",
    )  # active, on_notice, terminated, on_leave, absconding

    # ── Personal Details ─────────────────────────────────────
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    marital_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    blood_group: Mapped[str | None] = mapped_column(String(5), nullable=True)
    nationality: Mapped[str] = mapped_column(String(50), nullable=False, default="Indian")

    # ── Contact ──────────────────────────────────────────────
    personal_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    work_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    personal_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── Address ──────────────────────────────────────────────
    current_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    permanent_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")
    pin_code: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # ── Employment Dates ─────────────────────────────────────
    date_of_joining: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_confirmation: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_of_exit: Mapped[date | None] = mapped_column(Date, nullable=True)
    notice_period_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    # ── Compensation ─────────────────────────────────────────
    ctc: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    basic_salary: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bank_account_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ifsc_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pan_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    uan_number: Mapped[str | None] = mapped_column(String(20), nullable=True)  # PF UAN

    # ── Work ─────────────────────────────────────────────────
    work_location: Mapped[str] = mapped_column(String(100), default="Office", nullable=False)
    shift: Mapped[str] = mapped_column(String(50), default="General", nullable=False)

    # ── AI-generated ─────────────────────────────────────────
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ────────────────────────────────────────
    user = relationship("User", back_populates="employee", lazy="selectin")
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id], lazy="selectin")
    designation = relationship("Designation", back_populates="employees", lazy="selectin")
    reporting_manager = relationship("Employee", remote_side="Employee.id", lazy="selectin")
    documents = relationship("EmployeeDocument", back_populates="employee", lazy="noload", cascade="all, delete-orphan")
    skills = relationship("EmployeeSkill", back_populates="employee", lazy="selectin", cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContact", back_populates="employee", lazy="noload", cascade="all, delete-orphan")
    timeline = relationship("EmployeeTimeline", back_populates="employee", lazy="noload", cascade="all, delete-orphan")
    leave_balances = relationship("LeaveBalance", back_populates="employee", lazy="noload")
    leave_requests = relationship("LeaveRequest", back_populates="employee", lazy="noload")


class EmployeeDocument(BaseModel):
    """Employee uploaded documents (Aadhar, PAN, certificates, etc.)."""

    __tablename__ = "employee_documents"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    document_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verified_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    employee = relationship("Employee", back_populates="documents")


class EmployeeSkill(BaseModel):
    """Employee skill with proficiency level."""

    __tablename__ = "employee_skills"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    proficiency: Mapped[int] = mapped_column(Integer, default=3, nullable=False)  # 1-5
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    employee = relationship("Employee", back_populates="skills")


class EmergencyContact(BaseModel):
    """Employee emergency contact information."""

    __tablename__ = "emergency_contacts"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    relationship: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    alternate_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    employee = sa_orm.relationship("Employee", back_populates="emergency_contacts")


class EmployeeTimeline(BaseModel):
    """Timeline of significant events in an employee's tenure."""

    __tablename__ = "employee_timeline"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

    employee = relationship("Employee", back_populates="timeline")
