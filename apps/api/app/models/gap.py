import uuid
import enum

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class GapType(str, enum.Enum):
    missing_test = "missing_test"
    missing_evidence = "missing_evidence"
    failed_test = "failed_test"
    missing_security_validation = "missing_security_validation"
    missing_safety_validation = "missing_safety_validation"
    stale_evidence = "stale_evidence"
    unapproved_ai_suggestion = "unapproved_ai_suggestion"


class GapSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class GapStatus(str, enum.Enum):
    open = "open"
    acknowledged = "acknowledged"
    resolved = "resolved"


class Gap(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "gaps"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    gap_type: Mapped[GapType] = mapped_column(Enum(GapType), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[GapSeverity] = mapped_column(Enum(GapSeverity), nullable=False)
    status: Mapped[GapStatus] = mapped_column(Enum(GapStatus), nullable=False, default=GapStatus.open)
    related_requirement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requirements.id", ondelete="SET NULL")
    )
    related_test_case_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("test_cases.id", ondelete="SET NULL")
    )
    related_evidence_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evidence.id", ondelete="SET NULL")
    )
    ai_confidence: Mapped[float | None] = mapped_column(Float)
    recommendation: Mapped[str | None] = mapped_column(Text)
