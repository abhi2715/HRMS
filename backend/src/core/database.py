"""
Async SQLAlchemy database engine, session factory, and dependency injection.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def _import_all_models() -> None:
    """Import every model module so SQLAlchemy can resolve all relationships.

    This must run before any query is executed, otherwise cross-module
    relationships (e.g. User.employee → Employee) will fail with
    'failed to locate a name' errors.
    """
    import src.auth.models  # noqa: F401
    import src.employees.models  # noqa: F401
    import src.leaves.models  # noqa: F401
    import src.attendance.models  # noqa: F401
    import src.recruitment.models  # noqa: F401
    import src.payroll.models  # noqa: F401
    import src.performance.models  # noqa: F401
    import src.training.models  # noqa: F401
    import src.compliance.models  # noqa: F401


_import_all_models()

