from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.test_run import TestRunStatus


class TestRunResponse(BaseModel):
    id: UUID
    project_id: UUID
    test_case_id: UUID
    external_id: str | None
    status: TestRunStatus
    executed_at: datetime
    duration_seconds: float | None
    environment: str | None
    result_summary: str | None

    model_config = {"from_attributes": True}


class EvidenceResponse(BaseModel):
    id: UUID
    project_id: UUID
    source_document_id: UUID | None
    test_run_id: UUID | None
    title: str
    description: str | None
    evidence_type: str
    storage_uri: str | None
    hash: str | None
    created_by_user_id: UUID | None
    evidence_date: datetime

    model_config = {"from_attributes": True}


class EvidenceImportError(BaseModel):
    index: int
    external_test_id: str | None
    error: str


class EvidenceImportResult(BaseModel):
    imported: int
    skipped: int
    errors: list[EvidenceImportError]
    evidence: list[EvidenceResponse]
