from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ReadinessScoreResponse(BaseModel):
    id: UUID
    project_id: UUID
    overall_score: float
    coverage_score: float
    test_pass_score: float
    evidence_score: float
    risk_score: float
    freshness_score: float
    human_review_score: float
    critical_blocker_count: int
    high_gap_count: int
    medium_gap_count: int
    low_gap_count: int
    explanation: str
    caps_applied_json: list[Any]
    top_blockers_json: list[Any]
    recommended_actions_json: list[Any]
    created_at: datetime

    model_config = {"from_attributes": True}
