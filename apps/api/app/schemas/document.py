from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.document import DocumentSourceType, ProcessingStatus


class DocumentResponse(BaseModel):
    id: UUID
    project_id: UUID
    filename: str
    file_type: str
    source_type: DocumentSourceType
    file_hash: Optional[str]
    file_size_bytes: Optional[int]
    processing_status: ProcessingStatus
    extracted_text: Optional[str]
    processing_error: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
