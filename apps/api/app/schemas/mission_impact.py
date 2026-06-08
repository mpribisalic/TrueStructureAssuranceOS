from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.mission_impact import ImpactCategory, ImpactLevel


class MissionImpactRead(BaseModel):
    id: UUID
    project_id: UUID
    related_gap_id: UUID | None
    impact_category: ImpactCategory
    impact_level: ImpactLevel
    title: str
    operational_consequence: str
    mission_consequence: str
    readiness_delta: float
    created_at: datetime

    model_config = {"from_attributes": True}


class MissionImpactAnalyzeResponse(BaseModel):
    analyzed: int
    impacts: list[MissionImpactRead]
