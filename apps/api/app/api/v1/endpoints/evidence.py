import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.evidence import EvidenceImportResult, EvidenceResponse
from app.services import evidence_service

router = APIRouter(tags=["evidence"])


@router.post(
    "/projects/{project_id}/evidence/import",
    response_model=EvidenceImportResult,
    status_code=201,
)
async def import_evidence(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    source_document_id: uuid.UUID | None = Form(default=None),
):
    if not (file.filename or "").lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are accepted")
    data = await file.read()
    try:
        return evidence_service.import_json(db, project_id, source_document_id, data, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/projects/{project_id}/evidence", response_model=list[EvidenceResponse])
def list_evidence(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return evidence_service.list_evidence(db, project_id)


@router.get("/evidence/{evidence_id}", response_model=EvidenceResponse)
def get_evidence(
    evidence_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return evidence_service.get_evidence(db, evidence_id)
