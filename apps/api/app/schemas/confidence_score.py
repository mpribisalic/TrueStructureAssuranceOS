from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.confidence_score import ConfidenceLevel


class ConfidenceScoreRead(BaseModel):
    id: UUID
    project_id: UUID
    confidence_level: ConfidenceLevel
    confidence_value: float
    approved_traceability_ratio: float
    approved_requirements_ratio: float
    approved_evidence_ratio: float
    ai_only_decisions_ratio: float
    open_gaps_ratio: float
    explanation: str
    calculated_at: datetime

    model_config = {"from_attributes": True}


# Alias
ConfidenceScoreResponse = ConfidenceScoreRead
