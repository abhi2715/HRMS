"""
Recruitment module — SQLAlchemy models.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import BaseModel


class JobPosting(BaseModel):
    """Job opening / requisition."""

    __tablename__ = "job_postings"

    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True,
    )
    designation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("designations.id", ondelete="SET NULL"), nullable=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str] = mapped_column(Text, nullable=False)
    responsibilities: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_skills: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True)
    nice_to_have_skills: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True)
    employment_type: Mapped[str] = mapped_column(String(20), default="full_time", nullable=False)
    experience_min: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    experience_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    location: Mapped[str] = mapped_column(String(100), default="Bangalore", nullable=False)
    is_remote: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    positions: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    filled_positions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="draft", nullable=False, index=True,
    )  # draft, open, on_hold, closed, filled
    posted_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closing_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    department = relationship("Department", lazy="selectin")
    designation = relationship("Designation", lazy="selectin")
    candidates = relationship("Candidate", back_populates="job_posting", lazy="noload")


class Candidate(BaseModel):
    """Job candidate / applicant."""

    __tablename__ = "candidates"

    job_posting_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("job_postings.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    current_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    current_designation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_ctc: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    expected_ctc: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    notice_period_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="website", nullable=False)
    stage: Mapped[str] = mapped_column(
        String(30), default="applied", nullable=False, index=True,
    )  # applied, screening, shortlisted, interview, technical, hr_round, offer, hired, rejected
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-5
    skills_extracted: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True)
    ai_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    ai_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_skill_gaps: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    job_posting = relationship("JobPosting", back_populates="candidates", lazy="selectin")
    resumes = relationship("CandidateResume", back_populates="candidate", lazy="selectin", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="candidate", lazy="noload", cascade="all, delete-orphan")


class CandidateResume(BaseModel):
    """Uploaded resume for a candidate."""

    __tablename__ = "candidate_resumes"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parsed_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    embedding_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    candidate = relationship("Candidate", back_populates="resumes")


class Interview(BaseModel):
    """Interview scheduling and tracking."""

    __tablename__ = "interviews"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    interviewer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True,
    )
    round_name: Mapped[str] = mapped_column(String(50), nullable=False)  # screening, technical, hr, final
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    meeting_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), default="scheduled", nullable=False,
    )  # scheduled, completed, cancelled, no_show, rescheduled
    ai_questions: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    candidate = relationship("Candidate", back_populates="interviews")
    interviewer = relationship("Employee", lazy="selectin")
    feedback = relationship("InterviewFeedback", back_populates="interview", lazy="selectin", cascade="all, delete-orphan")


class InterviewFeedback(BaseModel):
    """Interview feedback from the interviewer."""

    __tablename__ = "interview_feedback"

    interview_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    interviewer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    technical_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    communication_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    problem_solving_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cultural_fit_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overall_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommendation: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )  # strong_hire, hire, no_hire, strong_no_hire
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    interview = relationship("Interview", back_populates="feedback")
