import uuid
import enum

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin


class ImpactCategory(str, enum.Enum):
    safety = "safety"
    cyber = "cyber"
    mission = "mission"
    availability = "availability"
    reliability = "reliability"
    compliance = "compliance"


class ImpactLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class MissionImpact(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "mission_impacts"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    related_gap_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gaps.id", ondelete="SET NULL"), nullable=True
    )
    impact_category: Mapped[ImpactCategory] = mapped_column(Enum(ImpactCategory), nullable=False)
    impact_level: Mapped[ImpactLevel] = mapped_column(Enum(ImpactLevel), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    operational_consequence: Mapped[str] = mapped_column(Text, nullable=False)
    mission_consequence: Mapped[str] = mapped_column(Text, nullable=False)
    readiness_delta: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    project: Mapped["app.models.project.Project"] = relationship("Project")
    gap: Mapped["app.models.gap.Gap | None"] = relationship("Gap")
