import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.mission_impact import MissionImpactAnalyzeResponse, MissionImpactRead
from app.services import mission_impact_service

router = APIRouter(tags=["mission-impact"])


@router.post(
    "/projects/{project_id}/mission-impact/analyze",
    response_model=MissionImpactAnalyzeResponse,
    status_code=201,
)
def analyze_mission_impact(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return mission_impact_service.analyze_mission_impact(db, project_id)


@router.get(
    "/projects/{project_id}/mission-impact",
    response_model=list[MissionImpactRead],
)
def list_mission_impacts(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return mission_impact_service.list_mission_impacts(db, project_id)
