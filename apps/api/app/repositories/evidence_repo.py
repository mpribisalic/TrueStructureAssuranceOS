import uuid

from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.models.test_run import TestRun


def create_test_run(db: Session, test_run: TestRun) -> TestRun:
    db.add(test_run)
    db.flush()
    return test_run


def create_evidence(db: Session, evidence: Evidence) -> Evidence:
    db.add(evidence)
    db.flush()
    return evidence


def get_evidence_all(db: Session, project_id: uuid.UUID) -> list[Evidence]:
    return (
        db.query(Evidence)
        .filter(Evidence.project_id == project_id)
        .order_by(Evidence.evidence_date.desc())
        .all()
    )


def get_evidence_by_id(db: Session, evidence_id: uuid.UUID) -> Evidence | None:
    return db.get(Evidence, evidence_id)
