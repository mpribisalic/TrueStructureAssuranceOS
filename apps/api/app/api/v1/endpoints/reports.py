import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.report import ReportCreate, ReportResponse
from app.services import report_service

router = APIRouter(tags=["reports"])


@router.post("/projects/{project_id}/reports", response_model=ReportResponse, status_code=201)
def create_report(
    project_id: uuid.UUID,
    payload: ReportCreate,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
):
    return report_service.create_report(db, project_id, payload, current_user.id)


@router.get("/projects/{project_id}/reports", response_model=list[ReportResponse])
def list_reports(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return report_service.list_reports(db, project_id)


@router.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return report_service.get_report(db, report_id)


@router.get("/reports/{report_id}/download")
def download_report(
    report_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    """Returns the raw Markdown content as a downloadable file."""
    report = report_service.get_report(db, report_id)
    filename = (
        report.title.encode("ascii", errors="ignore").decode()
        .replace(" ", "_").replace("/", "-")[:80] + ".md"
    )
    return Response(
        content=report.content_markdown or "",
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
