"""ATVP connector endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import RequireEngineer
from app.db.session import get_db
from app.schemas.atvp import ATVPImportRequest, ATVPImportResponse
from app.services import atvp_service

router = APIRouter(tags=["atvp"])


@router.post(
    "/projects/{project_id}/evidence/import-atvp",
    response_model=ATVPImportResponse,
    status_code=201,
)
def import_atvp(
    project_id: uuid.UUID,
    body: ATVPImportRequest,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
) -> ATVPImportResponse:
    try:
        return atvp_service.import_atvp_results(db, project_id, body, current_user.id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
