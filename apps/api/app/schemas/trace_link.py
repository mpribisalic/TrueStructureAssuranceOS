from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.requirement import HumanReviewStatus


class TraceLinkResponse(BaseModel):
    id: UUID
    project_id: UUID
    source_type: str
    source_id: UUID
    target_type: str
    target_id: UUID
    link_type: str
    confidence: float | None
    reason: str | None
    created_by: str
    human_review_status: HumanReviewStatus

    model_config = {"from_attributes": True}


class TraceLinkSuggestResult(BaseModel):
    suggested: int
    skipped: int
    links: list[TraceLinkResponse]


class TraceLinkCreate(BaseModel):
    source_id: UUID
    target_id: UUID
    target_type: str = "test_case"
    link_type: str = "verifies"
