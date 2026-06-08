import uuid
import enum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class TestCaseStatus(str, enum.Enum):
    active = "active"
    deprecated = "deprecated"


class TestCase(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "test_cases"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL")
    )
    external_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    # e.g. system, unit, integration, simulation, inspection, analysis, security
    test_type: Mapped[str] = mapped_column(String(100), nullable=False, default="system")
    # e.g. automated, manual, semi-automated
    automation_level: Mapped[str] = mapped_column(String(100), nullable=False, default="manual")
    status: Mapped[TestCaseStatus] = mapped_column(
        Enum(TestCaseStatus), nullable=False, default=TestCaseStatus.active
    )
