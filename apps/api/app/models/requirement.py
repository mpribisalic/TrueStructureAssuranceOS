import uuid
import enum

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class RequirementCriticality(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
    catastrophic = "catastrophic"


class HumanReviewStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RequirementStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    deprecated = "deprecated"


class Requirement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "requirements"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL")
    )
    external_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="functional")
    criticality: Mapped[RequirementCriticality] = mapped_column(
        Enum(RequirementCriticality), nullable=False, default=RequirementCriticality.medium
    )
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    verification_method: Mapped[str] = mapped_column(String(100), nullable=False, default="test")
    status: Mapped[RequirementStatus] = mapped_column(
        Enum(RequirementStatus), nullable=False, default=RequirementStatus.active
    )
    # Null when created manually; populated when extracted by AI
    ai_confidence: Mapped[float | None] = mapped_column(Float)
    source_reference: Mapped[str | None] = mapped_column(String(500))
    human_review_status: Mapped[HumanReviewStatus] = mapped_column(
        Enum(HumanReviewStatus), nullable=False, default=HumanReviewStatus.pending
    )
