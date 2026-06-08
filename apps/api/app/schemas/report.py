from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: UUID
    project_id: UUID
    readiness_score_id: UUID | None
    title: str
    report_type: str
    format: str
    storage_uri: str | None
    content_markdown: str | None
    created_by_user_id: UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportCreate(BaseModel):
    title: str | None = None
    report_type: str = "readiness"
