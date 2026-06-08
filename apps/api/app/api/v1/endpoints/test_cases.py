import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, RequireEngineer
from app.db.session import get_db
from app.schemas.test_case import TestCaseImportResult, TestCaseResponse
from app.services import test_case_service

router = APIRouter(tags=["test-cases"])


@router.post(
    "/projects/{project_id}/test-cases/import",
    response_model=TestCaseImportResult,
    status_code=201,
)
async def import_test_cases(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    source_document_id: uuid.UUID | None = Form(default=None),
):
    if not (file.filename or "").lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    data = await file.read()
    try:
        return test_case_service.import_csv(db, project_id, source_document_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/projects/{project_id}/test-cases", response_model=list[TestCaseResponse])
def list_test_cases(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return test_case_service.list_test_cases(db, project_id)


@router.get("/test-cases/{test_case_id}", response_model=TestCaseResponse)
def get_test_case(
    test_case_id: uuid.UUID,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return test_case_service.get_test_case(db, test_case_id)
