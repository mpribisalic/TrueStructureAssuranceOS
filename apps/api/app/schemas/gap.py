from uuid import UUID

from pydantic import BaseModel

from app.models.gap import GapSeverity, GapStatus, GapType


class GapResponse(BaseModel):
    id: UUID
    project_id: UUID
    gap_type: GapType
    title: str
    description: str
    severity: GapSeverity
    status: GapStatus
    related_requirement_id: UUID | None
    related_test_case_id: UUID | None
    related_evidence_id: UUID | None
    ai_confidence: float | None
    recommendation: str | None

    model_config = {"from_attributes": True}


class GapUpdate(BaseModel):
    status: GapStatus | None = None
    recommendation: str | None = None


class GapDetectResult(BaseModel):
    detected: int
    gaps: list[GapResponse]
