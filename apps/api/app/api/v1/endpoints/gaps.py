import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.gap import GapDetectResult, GapResponse, GapUpdate
from app.services import gap_service

router = APIRouter(tags=["gaps"])


@router.post(
    "/projects/{project_id}/gaps/detect",
    response_model=GapDetectResult,
    status_code=201,
)
def detect_gaps(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return gap_service.detect_gaps(db, project_id)


@router.get("/projects/{project_id}/gaps", response_model=list[GapResponse])
def list_gaps(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return gap_service.list_gaps(db, project_id)


@router.patch("/gaps/{gap_id}", response_model=GapResponse)
def update_gap(
    gap_id: uuid.UUID,
    payload: GapUpdate,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return gap_service.update_gap(db, gap_id, payload)
