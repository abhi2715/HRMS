"""
Performance management — SQLAlchemy models.
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


class PerformanceGoal(BaseModel):
    """Employee performance goals / OKRs."""

    __tablename__ = "performance_goals"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), default="individual", nullable=False)
    key_results: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=100, nullable=False)
    target_value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    current_value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0-100
    status: Mapped[str] = mapped_column(
        String(20), default="not_started", nullable=False,
    )  # not_started, in_progress, completed, deferred
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    review_period: Mapped[str] = mapped_column(String(20), default="Q1", nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    employee = relationship("Employee", lazy="selectin")


class PerformanceReview(BaseModel):
    """Performance review cycle entry."""

    __tablename__ = "performance_reviews"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True,
    )
    review_period: Mapped[str] = mapped_column(String(20), nullable=False)  # Q1, Q2, H1, Annual
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    review_type: Mapped[str] = mapped_column(
        String(30), default="annual", nullable=False,
    )  # annual, mid_year, quarterly, probation
    self_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    manager_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    final_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    self_comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    manager_comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    goals_achieved: Mapped[int | None] = mapped_column(Integer, nullable=True)
    goals_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    areas_of_improvement: Mapped[str | None] = mapped_column(Text, nullable=True)
    promotion_recommendation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False,
    )  # pending, self_review, manager_review, completed, acknowledged
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_promotion_suggestion: Mapped[str | None] = mapped_column(Text, nullable=True)

    employee = relationship("Employee", foreign_keys=[employee_id], lazy="selectin")
    reviewer = relationship("Employee", foreign_keys=[reviewer_id], lazy="selectin")
    feedbacks = relationship("ReviewFeedback", back_populates="review", lazy="selectin", cascade="all, delete-orphan")


class ReviewFeedback(BaseModel):
    """360-degree feedback for a performance review."""

    __tablename__ = "review_feedbacks"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("performance_reviews.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    feedback_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    feedback_type: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )  # peer, manager, subordinate, self
    rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    improvements: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    review = relationship("PerformanceReview", back_populates="feedbacks")
