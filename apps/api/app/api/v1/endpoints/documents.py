import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db  # noqa: F401 (used via Depends)
from app.models.document import DocumentSourceType
from app.schemas.document import DocumentResponse
from app.services import document_service

router = APIRouter(tags=["documents"])


@router.post(
    "/projects/{project_id}/documents",
    response_model=DocumentResponse,
    status_code=201,
)
async def upload_document(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    source_type: DocumentSourceType = Form(DocumentSourceType.other),
):
    data = await file.read()
    return document_service.upload_document(
        db, project_id, file.filename or "upload", data, source_type, current_user
    )


@router.get("/projects/{project_id}/documents", response_model=list[DocumentResponse])
def list_documents(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return document_service.list_documents(db, project_id)


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return document_service.get_document(db, document_id)


@router.post("/documents/{document_id}/process", response_model=DocumentResponse)
def reprocess_document(
    document_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return document_service.reprocess_document(db, document_id)
