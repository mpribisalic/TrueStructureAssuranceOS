import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.trace_link import TraceLinkResponse, TraceLinkSuggestResult
from app.services import trace_link_service

router = APIRouter(tags=["traceability"])


@router.post(
    "/projects/{project_id}/trace-links/suggest",
    response_model=TraceLinkSuggestResult,
    status_code=201,
)
def suggest_trace_links(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return trace_link_service.suggest_links(db, project_id)


@router.get("/projects/{project_id}/trace-links", response_model=list[TraceLinkResponse])
def list_trace_links(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return trace_link_service.list_links(db, project_id)


@router.post("/trace-links/{link_id}/approve", response_model=TraceLinkResponse)
def approve_trace_link(
    link_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return trace_link_service.approve_link(db, link_id)


@router.post("/trace-links/{link_id}/reject", response_model=TraceLinkResponse)
def reject_trace_link(
    link_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return trace_link_service.reject_link(db, link_id)
