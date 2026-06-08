import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireAdmin, RequireEngineer
from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectResponse])
def list_projects(current_user: CurrentUser, db: Annotated[Session, Depends(get_db)]):
    return project_service.list_projects(db, current_user)


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    data: ProjectCreate,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return project_service.create_project(db, data, current_user)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return project_service.get_project(db, project_id, current_user)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return project_service.update_project(db, project_id, data, current_user)


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: uuid.UUID,
    current_user: RequireAdmin,
    db: Annotated[Session, Depends(get_db)],
):
    project_service.delete_project(db, project_id, current_user)
