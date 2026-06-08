from uuid import UUID

from pydantic import BaseModel

from app.models.test_case import TestCaseStatus


class TestCaseResponse(BaseModel):
    id: UUID
    project_id: UUID
    source_document_id: UUID | None
    external_id: str
    title: str
    description: str | None
    test_type: str
    automation_level: str
    status: TestCaseStatus

    model_config = {"from_attributes": True}


class TestCaseImportError(BaseModel):
    row: int
    external_id: str | None
    error: str


class TestCaseImportResult(BaseModel):
    imported: int
    skipped: int
    errors: list[TestCaseImportError]
    test_cases: list[TestCaseResponse]
