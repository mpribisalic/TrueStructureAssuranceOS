import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.requirement import RequirementCreate, RequirementResponse, RequirementUpdate
from app.services import requirement_service

router = APIRouter(tags=["requirements"])


@router.post(
    "/documents/{document_id}/extract-requirements",
    response_model=list[RequirementResponse],
    status_code=201,
)
def extract_requirements(
    document_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.extract_requirements(db, document_id)


@router.get("/projects/{project_id}/requirements", response_model=list[RequirementResponse])
def list_requirements(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.list_requirements(db, project_id)


@router.post(
    "/projects/{project_id}/requirements",
    response_model=RequirementResponse,
    status_code=201,
)
def create_requirement(
    project_id: uuid.UUID,
    payload: RequirementCreate,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.create_requirement(db, project_id, payload)


@router.patch("/requirements/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
    requirement_id: uuid.UUID,
    payload: RequirementUpdate,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.update_requirement(db, requirement_id, payload)


@router.post("/requirements/{requirement_id}/approve", response_model=RequirementResponse)
def approve_requirement(
    requirement_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.approve_requirement(db, requirement_id)


@router.post("/requirements/{requirement_id}/reject", response_model=RequirementResponse)
def reject_requirement(
    requirement_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return requirement_service.reject_requirement(db, requirement_id)
