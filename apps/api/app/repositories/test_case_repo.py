import uuid

from sqlalchemy.orm import Session

from app.models.test_case import TestCase


def create(db: Session, test_case: TestCase) -> TestCase:
    db.add(test_case)
    db.flush()
    return test_case


def get_all(db: Session, project_id: uuid.UUID) -> list[TestCase]:
    return (
        db.query(TestCase)
        .filter(TestCase.project_id == project_id)
        .order_by(TestCase.external_id)
        .all()
    )


def get_by_id(db: Session, test_case_id: uuid.UUID) -> TestCase | None:
    return db.get(TestCase, test_case_id)


def get_by_external_id(
    db: Session, project_id: uuid.UUID, external_id: str
) -> TestCase | None:
    return (
        db.query(TestCase)
        .filter(
            TestCase.project_id == project_id,
            TestCase.external_id == external_id,
        )
        .first()
    )
