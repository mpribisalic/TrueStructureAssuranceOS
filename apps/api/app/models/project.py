import uuid
import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.organization import Organization


class Industry(str, enum.Enum):
    defense = "defense"
    aerospace = "aerospace"
    medical = "medical"
    railway = "railway"
    industrial = "industrial"
    automotive = "automotive"
    space = "space"
    robotics = "robotics"
    energy = "energy"
    other = "other"


class CriticalityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    mission_critical = "mission_critical"
    safety_critical = "safety_critical"


class ProjectStatus(str, enum.Enum):
    active = "active"
    archived = "archived"


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    industry: Mapped[Industry] = mapped_column(Enum(Industry), nullable=False, default=Industry.other)
    system_type: Mapped[str | None] = mapped_column(String(255))
    criticality_level: Mapped[CriticalityLevel] = mapped_column(
        Enum(CriticalityLevel), nullable=False, default=CriticalityLevel.medium
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False, default=ProjectStatus.active
    )

    organization: Mapped["Organization"] = relationship("Organization", back_populates="projects")
