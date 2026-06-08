import uuid
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin

if False:  # TYPE_CHECKING
    from app.models.test_case import TestCase


class TestRunStatus(str, enum.Enum):
    passed = "passed"
    failed = "failed"
    blocked = "blocked"
    skipped = "skipped"


class TestRun(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Immutable record of a single test case execution. Never updated after creation."""
    __tablename__ = "test_runs"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    test_case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    external_id: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[TestRunStatus] = mapped_column(Enum(TestRunStatus), nullable=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    environment: Mapped[str | None] = mapped_column(String(255))
    result_summary: Mapped[str | None] = mapped_column(Text)
    raw_result_uri: Mapped[str | None] = mapped_column(String(1000))

    test_case: Mapped["TestCase"] = relationship("TestCase")
