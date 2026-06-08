import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.readiness import ReadinessScoreResponse
from app.services import readiness_service

router = APIRouter(tags=["readiness"])


@router.post(
    "/projects/{project_id}/readiness/calculate",
    response_model=ReadinessScoreResponse,
    status_code=201,
)
def calculate_readiness(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return readiness_service.calculate(db, project_id)


@router.get("/projects/{project_id}/readiness/latest", response_model=ReadinessScoreResponse)
def get_latest_readiness(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return readiness_service.get_latest(db, project_id)


@router.get(
    "/projects/{project_id}/readiness/history",
    response_model=list[ReadinessScoreResponse],
)
def get_readiness_history(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return readiness_service.get_history(db, project_id)
