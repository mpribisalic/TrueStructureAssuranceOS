"""CSV import and CRUD for test cases."""
import csv
import io
import uuid

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.test_case import TestCase, TestCaseStatus
from app.repositories import test_case_repo
from app.schemas.test_case import TestCaseImportError, TestCaseImportResult

_REQUIRED_COLUMNS = {"external_id", "title"}
_VALID_TEST_TYPES = {"system", "unit", "integration", "simulation", "inspection", "analysis", "security", "safety"}
_VALID_AUTOMATION = {"automated", "manual", "semi-automated"}
_VALID_STATUSES = {"active", "deprecated"}


def import_csv(
    db: Session,
    project_id: uuid.UUID,
    source_document_id: uuid.UUID | None,
    data: bytes,
) -> TestCaseImportResult:
    text = data.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    if not reader.fieldnames or not _REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
        missing = _REQUIRED_COLUMNS - set(reader.fieldnames or [])
        raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing))}")

    imported: list[TestCase] = []
    errors: list[TestCaseImportError] = []
    skipped = 0

    for row_num, row in enumerate(reader, start=2):
        external_id = (row.get("external_id") or "").strip()
        title = (row.get("title") or "").strip()

        if not external_id or not title:
            errors.append(TestCaseImportError(row=row_num, external_id=external_id or None, error="external_id and title are required"))
            continue

        test_type = (row.get("test_type") or "system").strip().lower()
        automation_level = (row.get("automation_level") or "manual").strip().lower()
        status_raw = (row.get("status") or "active").strip().lower()

        if test_type not in _VALID_TEST_TYPES:
            errors.append(TestCaseImportError(row=row_num, external_id=external_id, error=f"invalid test_type: {test_type}"))
            continue
        if automation_level not in _VALID_AUTOMATION:
            errors.append(TestCaseImportError(row=row_num, external_id=external_id, error=f"invalid automation_level: {automation_level}"))
            continue
        if status_raw not in _VALID_STATUSES:
            errors.append(TestCaseImportError(row=row_num, external_id=external_id, error=f"invalid status: {status_raw}"))
            continue

        # Skip duplicates silently
        if test_case_repo.get_by_external_id(db, project_id, external_id):
            skipped += 1
            continue

        tc = TestCase(
            project_id=project_id,
            source_document_id=source_document_id,
            external_id=external_id,
            title=title,
            description=(row.get("description") or "").strip() or None,
            test_type=test_type,
            automation_level=automation_level,
            status=TestCaseStatus(status_raw),
        )
        test_case_repo.create(db, tc)
        imported.append(tc)

    db.flush()
    return TestCaseImportResult(
        imported=len(imported),
        skipped=skipped,
        errors=errors,
        test_cases=imported,
    )


def list_test_cases(db: Session, project_id: uuid.UUID) -> list[TestCase]:
    return test_case_repo.get_all(db, project_id)


def get_test_case(db: Session, test_case_id: uuid.UUID) -> TestCase:
    tc = test_case_repo.get_by_id(db, test_case_id)
    if not tc:
        raise NotFoundError("Test case not found")
    return tc
