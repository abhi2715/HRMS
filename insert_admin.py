import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from passlib.context import CryptContext
from src.core.config import get_settings

from src.auth.models import User
from src.employees.models import Employee, Department
from src.performance.models import PerformanceGoal, PerformanceReview
from src.training.models import TrainingCourse, CourseEnrollment

settings = get_settings()
engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def main():
    async with async_session() as session:
        user = User(
            email="rajesh.kumar@hrcopilot.io",
            hashed_password=pwd_context.hash("admin123"),
            full_name="Rajesh Kumar",
            role="admin",
            is_active=True
        )
        session.add(user)
        await session.commit()
        print("Admin user created!")

asyncio.run(main())
