import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import RequireEngineer
from app.db.session import get_db
from app.schemas.confidence_score import ConfidenceScoreRead
from app.services import confidence_service

router = APIRouter(tags=["confidence"])


@router.post(
    "/projects/{project_id}/confidence/calculate",
    response_model=ConfidenceScoreRead,
    status_code=201,
)
def calculate_confidence(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return confidence_service.calculate_confidence(db, project_id)


@router.get(
    "/projects/{project_id}/confidence",
    response_model=ConfidenceScoreRead,
)
def get_confidence(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return confidence_service.get_latest(db, project_id)
