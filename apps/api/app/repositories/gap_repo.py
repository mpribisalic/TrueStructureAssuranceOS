import uuid

from sqlalchemy.orm import Session

from app.models.gap import Gap, GapType


def create(db: Session, gap: Gap) -> Gap:
    db.add(gap)
    db.flush()
    return gap


def get_all(db: Session, project_id: uuid.UUID) -> list[Gap]:
    return (
        db.query(Gap)
        .filter(Gap.project_id == project_id)
        .order_by(Gap.severity.desc(), Gap.created_at.desc())
        .all()
    )


def get_by_id(db: Session, gap_id: uuid.UUID) -> Gap | None:
    return db.get(Gap, gap_id)


def exists(
    db: Session,
    project_id: uuid.UUID,
    gap_type: GapType,
    related_requirement_id: uuid.UUID | None,
    related_test_case_id: uuid.UUID | None = None,
) -> bool:
    q = db.query(Gap).filter(
        Gap.project_id == project_id,
        Gap.gap_type == gap_type,
        Gap.related_requirement_id == related_requirement_id,
    )
    if related_test_case_id is not None:
        q = q.filter(Gap.related_test_case_id == related_test_case_id)
    return q.first() is not None


def delete_all(db: Session, project_id: uuid.UUID) -> None:
    db.query(Gap).filter(Gap.project_id == project_id).delete()
    db.flush()
