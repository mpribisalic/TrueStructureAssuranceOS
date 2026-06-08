"""ATVP Connector: imports ATVP simulation results as Evidence + TestRun records."""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.models.test_case import TestCase, TestCaseStatus
from app.models.test_run import TestRun, TestRunStatus
from app.repositories import evidence_repo
from app.repositories.test_case_repo import get_by_external_id as get_tc_by_ext
from app.schemas.atvp import ATVPImportRequest, ATVPImportResponse

_STATUS_MAP = {
    "PASSED": TestRunStatus.passed,
    "FAILED": TestRunStatus.failed,
    "ERROR": TestRunStatus.failed,
}


def import_atvp_results(
    db: Session,
    project_id: uuid.UUID,
    data: ATVPImportRequest,
    user_id: uuid.UUID,
) -> ATVPImportResponse:
    imported = 0
    skipped = 0
    errors: list[str] = []
    evidence_ids: list[str] = []

    export_ts = data.export_timestamp or datetime.now(timezone.utc)

    for result in data.results:
        try:
            # Idempotency: skip if a TestRun with same external_id already exists for this project
            existing = (
                db.query(TestRun)
                .filter(
                    TestRun.project_id == project_id,
                    TestRun.external_id == result.test_id,
                )
                .first()
            )
            if existing:
                skipped += 1
                continue

            mapped_status = _STATUS_MAP.get(result.status.upper(), TestRunStatus.failed)
            executed_at = result.timestamp or export_ts

            # Find or create a TestCase for this ATVP test id
            test_case = get_tc_by_ext(db, project_id, result.test_id)
            if not test_case:
                test_case = TestCase(
                    project_id=project_id,
                    external_id=result.test_id,
                    title=result.test_name,
                    description=f"Auto-created from ATVP import: {data.scenario or 'unknown scenario'}",
                    test_type="simulation",
                    automation_level="automated",
                    status=TestCaseStatus.active,
                )
                db.add(test_case)
                db.flush()

            # Build notes combining result.notes and metric info
            notes_parts = []
            if result.notes:
                notes_parts.append(result.notes)
            if result.metric is not None:
                metric_info = f"{result.metric}"
                if result.expected is not None:
                    metric_info += f": expected={result.expected}"
                if result.actual is not None:
                    metric_info += f", actual={result.actual}"
                notes_parts.append(metric_info)
            notes = ". ".join(notes_parts) if notes_parts else None

            test_run = TestRun(
                project_id=project_id,
                test_case_id=test_case.id,
                external_id=result.test_id,
                status=mapped_status,
                executed_at=executed_at,
                result_summary=notes,
            )
            evidence_repo.create_test_run(db, test_run)

            # Build evidence description
            score_str = f" Score: {result.score}." if result.score is not None else ""
            description = f"Scenario: {data.scenario or 'N/A'}. {result.notes or ''}.{score_str}".strip()

            evidence = Evidence(
                project_id=project_id,
                test_run_id=test_run.id,
                title=f"ATVP: {result.test_name}",
                description=description,
                evidence_type="test_result",
                created_by_user_id=user_id,
                evidence_date=executed_at,
            )
            evidence_repo.create_evidence(db, evidence)
            evidence_ids.append(str(evidence.id))
            imported += 1

        except Exception as exc:  # noqa: BLE001
            errors.append(f"{result.test_id}: {exc}")

    db.flush()

    message = (
        f"Imported {imported} ATVP result(s), skipped {skipped} duplicate(s)."
        if not errors
        else f"Imported {imported}, skipped {skipped}, {len(errors)} error(s)."
    )
    return ATVPImportResponse(
        imported=imported,
        skipped=skipped,
        errors=errors,
        evidence_ids=evidence_ids,
        message=message,
    )
