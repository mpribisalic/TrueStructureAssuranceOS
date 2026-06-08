import uuid

from sqlalchemy.orm import Session

from app.models.requirement import HumanReviewStatus, Requirement


def create(db: Session, requirement: Requirement) -> Requirement:
    db.add(requirement)
    db.flush()
    return requirement


def get_all(db: Session, project_id: uuid.UUID) -> list[Requirement]:
    return (
        db.query(Requirement)
        .filter(Requirement.project_id == project_id)
        .order_by(Requirement.external_id)
        .all()
    )


def get_by_id(db: Session, requirement_id: uuid.UUID) -> Requirement | None:
    return db.get(Requirement, requirement_id)


def get_by_external_id(
    db: Session, project_id: uuid.UUID, external_id: str
) -> Requirement | None:
    return (
        db.query(Requirement)
        .filter(
            Requirement.project_id == project_id,
            Requirement.external_id == external_id,
        )
        .first()
    )
