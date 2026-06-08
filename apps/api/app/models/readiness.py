import uuid
from typing import Any

from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class ReadinessScore(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Immutable snapshot of a readiness calculation at a point in time. Never updated."""
    __tablename__ = "readiness_scores"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    coverage_score: Mapped[float] = mapped_column(Float, nullable=False)
    test_pass_score: Mapped[float] = mapped_column(Float, nullable=False)
    evidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    freshness_score: Mapped[float] = mapped_column(Float, nullable=False)
    human_review_score: Mapped[float] = mapped_column(Float, nullable=False)
    critical_blocker_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    high_gap_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    medium_gap_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    low_gap_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    caps_applied_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    top_blockers_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    recommended_actions_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
