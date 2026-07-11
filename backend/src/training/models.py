"""
Training module — SQLAlchemy models.
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import BaseModel


class TrainingCourse(BaseModel):
    """Training course / program."""

    __tablename__ = "training_courses"

    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    skills_covered: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True)
    duration_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    instructor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    mode: Mapped[str] = mapped_column(String(20), default="online", nullable=False)
    content_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty_level: Mapped[str] = mapped_column(String(20), default="beginner", nullable=False)
    max_enrollments: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    certification_name: Mapped[str | None] = mapped_column(String(200), nullable=True)

    enrollments = relationship("CourseEnrollment", back_populates="course", lazy="noload")
    learning_paths = relationship("LearningPathCourse", back_populates="course", lazy="noload")


class LearningPath(BaseModel):
    """Curated learning path combining multiple courses."""

    __tablename__ = "learning_paths"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    skills_developed: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True)
    estimated_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    courses = relationship("LearningPathCourse", back_populates="learning_path", lazy="selectin")


class LearningPathCourse(BaseModel):
    """Course within a learning path (ordered)."""

    __tablename__ = "learning_path_courses"

    learning_path_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("learning_paths.id", ondelete="CASCADE"),
        nullable=False,
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("training_courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    learning_path = relationship("LearningPath", back_populates="courses")
    course = relationship("TrainingCourse", back_populates="learning_paths", lazy="selectin")


class CourseEnrollment(BaseModel):
    """Employee enrollment in a training course."""

    __tablename__ = "course_enrollments"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("training_courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="enrolled", nullable=False,
    )  # enrolled, in_progress, completed, dropped
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    certificate_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_recommended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    course = relationship("TrainingCourse", back_populates="enrollments", lazy="selectin")
