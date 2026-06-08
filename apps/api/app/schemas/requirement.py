from uuid import UUID

from pydantic import BaseModel

from app.models.requirement import HumanReviewStatus, RequirementCriticality, RequirementStatus


class RequirementResponse(BaseModel):
    id: UUID
    project_id: UUID
    source_document_id: UUID | None
    external_id: str
    title: str
    text: str
    category: str
    criticality: RequirementCriticality
    priority: str
    verification_method: str
    status: RequirementStatus
    ai_confidence: float | None
    source_reference: str | None
    human_review_status: HumanReviewStatus

    model_config = {"from_attributes": True}


class RequirementUpdate(BaseModel):
    title: str | None = None
    text: str | None = None
    category: str | None = None
    criticality: RequirementCriticality | None = None
    priority: str | None = None
    verification_method: str | None = None
    status: RequirementStatus | None = None


class RequirementCreate(BaseModel):
    external_id: str
    title: str
    text: str
    category: str = "functional"
    criticality: RequirementCriticality = RequirementCriticality.medium
    priority: str = "medium"
    verification_method: str = "test"
