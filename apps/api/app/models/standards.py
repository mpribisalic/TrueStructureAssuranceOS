import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class StandardType(str, enum.Enum):
    nato_stanag = "nato_stanag"
    do_178c = "do_178c"
    do_254 = "do_254"
    iso_26262 = "iso_26262"
    iec_61508 = "iec_61508"
    iec_62304 = "iec_62304"
    en_50128 = "en_50128"
    custom = "custom"


class Standard(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "standards"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    standard_type: Mapped[StandardType] = mapped_column(
        Enum(StandardType), nullable=False
    )
    version: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    clauses: Mapped[list["StandardClause"]] = relationship(
        "StandardClause", back_populates="standard", cascade="all, delete-orphan"
    )


class StandardClause(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "standard_clauses"

    standard_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("standards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    clause_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    standard: Mapped["Standard"] = relationship("Standard", back_populates="clauses")


class RequirementStandardLink(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "requirement_standard_links"

    requirement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    standard_clause_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("standard_clauses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    coverage_status: Mapped[str] = mapped_column(String(50), nullable=False, default="partial")
    notes: Mapped[str | None] = mapped_column(Text)
