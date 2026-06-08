import uuid

from sqlalchemy.orm import Session

from app.models.readiness import ReadinessScore


def create(db: Session, score: ReadinessScore) -> ReadinessScore:
    db.add(score)
    db.flush()
    return score


def get_latest(db: Session, project_id: uuid.UUID) -> ReadinessScore | None:
    return (
        db.query(ReadinessScore)
        .filter(ReadinessScore.project_id == project_id)
        .order_by(ReadinessScore.created_at.desc())
        .first()
    )


def get_history(db: Session, project_id: uuid.UUID) -> list[ReadinessScore]:
    return (
        db.query(ReadinessScore)
        .filter(ReadinessScore.project_id == project_id)
        .order_by(ReadinessScore.created_at.desc())
        .all()
    )
