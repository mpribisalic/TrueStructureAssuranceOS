"""Evidence JSON import: creates TestRun + Evidence records linked to TestCases."""
import json
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.evidence import Evidence
from app.models.test_run import TestRun, TestRunStatus
from app.repositories import evidence_repo
from app.repositories.test_case_repo import get_by_external_id as get_tc_by_ext
from app.schemas.evidence import EvidenceImportError, EvidenceImportResult

_VALID_STATUSES = {s.value for s in TestRunStatus}


def import_json(
    db: Session,
    project_id: uuid.UUID,
    source_document_id: uuid.UUID | None,
    data: bytes,
    imported_by_user_id: uuid.UUID,
) -> EvidenceImportResult:
    try:
        records = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(records, list):
        raise ValueError("Evidence JSON must be an array of objects")

    imported: list[Evidence] = []
    errors: list[EvidenceImportError] = []
    skipped = 0

    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(EvidenceImportError(index=idx, external_test_id=None, error="Each entry must be a JSON object"))
            continue

        ext_test_id = (record.get("external_test_id") or "").strip()
        status_raw = (record.get("status") or "").strip().lower()

        if not ext_test_id:
            errors.append(EvidenceImportError(index=idx, external_test_id=None, error="external_test_id is required"))
            continue
        if status_raw not in _VALID_STATUSES:
            errors.append(EvidenceImportError(index=idx, external_test_id=ext_test_id, error=f"invalid status: {status_raw!r}"))
            continue

        test_case = get_tc_by_ext(db, project_id, ext_test_id)
        if not test_case:
            errors.append(EvidenceImportError(index=idx, external_test_id=ext_test_id, error=f"test case not found: {ext_test_id}"))
            continue

        executed_at = _parse_dt(record.get("executed_at")) or datetime.now(timezone.utc)
        environment = (record.get("environment") or "").strip() or None
        summary = (record.get("summary") or "").strip() or None

        test_run = TestRun(
            project_id=project_id,
            test_case_id=test_case.id,
            external_id=ext_test_id,
            status=TestRunStatus(status_raw),
            executed_at=executed_at,
            environment=environment,
            result_summary=summary,
        )
        evidence_repo.create_test_run(db, test_run)

        evidence = Evidence(
            project_id=project_id,
            source_document_id=source_document_id,
            test_run_id=test_run.id,
            title=f"Test result: {ext_test_id} — {status_raw}",
            description=summary,
            evidence_type="test_result",
            created_by_user_id=imported_by_user_id,
            evidence_date=executed_at,
        )
        evidence_repo.create_evidence(db, evidence)
        imported.append(evidence)

    db.flush()
    return EvidenceImportResult(
        imported=len(imported),
        skipped=skipped,
        errors=errors,
        evidence=imported,
    )


def list_evidence(db: Session, project_id: uuid.UUID) -> list[Evidence]:
    return evidence_repo.get_evidence_all(db, project_id)


def get_evidence(db: Session, evidence_id: uuid.UUID) -> Evidence:
    ev = evidence_repo.get_evidence_by_id(db, evidence_id)
    if not ev:
        raise NotFoundError("Evidence not found")
    return ev


def _parse_dt(value) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
