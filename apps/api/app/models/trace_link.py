import uuid
import enum

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.requirement import HumanReviewStatus


class TraceLink(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "trace_links"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # source is always a requirement in TRL 4
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, default="requirement")
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # target is a test case or evidence item
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    # e.g. verifies, validates, demonstrates, supports
    link_type: Mapped[str] = mapped_column(String(100), nullable=False, default="verifies")
    # Null when created manually
    confidence: Mapped[float | None] = mapped_column(Float)
    reason: Mapped[str | None] = mapped_column(Text)
    # "ai" or "user"
    created_by: Mapped[str] = mapped_column(String(50), nullable=False, default="user")
    human_review_status: Mapped[HumanReviewStatus] = mapped_column(
        Enum(HumanReviewStatus), nullable=False, default=HumanReviewStatus.pending
    )
