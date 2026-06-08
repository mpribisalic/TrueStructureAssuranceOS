import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import Enum, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class ConfidenceLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    very_high = "very_high"


class ConfidenceScore(UUIDPrimaryKeyMixin, Base):
    """Single-row-per-project confidence snapshot. Previous rows are deleted on recalculation."""
    __tablename__ = "confidence_scores"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    confidence_level: Mapped[ConfidenceLevel] = mapped_column(
        Enum(ConfidenceLevel), nullable=False
    )
    confidence_value: Mapped[float] = mapped_column(Float, nullable=False)
    approved_traceability_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    approved_requirements_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    approved_evidence_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    ai_only_decisions_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    open_gaps_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )

    project = relationship("Project", back_populates=None, foreign_keys=[project_id])
