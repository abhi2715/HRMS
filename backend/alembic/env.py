"""
Alembic environment configuration for async SQLAlchemy migrations.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.core.config import get_settings
from src.core.database import Base

# Import ALL models so Alembic can detect them
from src.auth.models import AuditLog, Permission, Role, RolePermission, User  # noqa: F401
from src.employees.models import (  # noqa: F401
    Department, Designation, Employee, EmployeeDocument,
    EmployeeSkill, EmergencyContact, EmployeeTimeline,
)
from src.leaves.models import Holiday, LeaveBalance, LeaveRequest, LeaveType  # noqa: F401
from src.attendance.models import AttendanceRecord, Shift, ShiftAssignment  # noqa: F401
from src.recruitment.models import (  # noqa: F401
    Candidate, CandidateResume, Interview, InterviewFeedback, JobPosting,
)
from src.payroll.models import Payslip, PayrollRun, SalaryStructure, TaxDeclaration  # noqa: F401
from src.performance.models import PerformanceGoal, PerformanceReview, ReviewFeedback  # noqa: F401
from src.training.models import CourseEnrollment, LearningPath, LearningPathCourse, TrainingCourse  # noqa: F401
from src.compliance.models import CompliancePolicy, Notification, PolicyAcknowledgment  # noqa: F401

settings = get_settings()

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — generates SQL without connecting."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.database_url
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations online."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
