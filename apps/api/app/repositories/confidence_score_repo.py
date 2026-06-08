import uuid

from sqlalchemy.orm import Session

from app.models.confidence_score import ConfidenceScore


def create(db: Session, score: ConfidenceScore) -> ConfidenceScore:
    db.add(score)
    db.flush()
    return score


def get_latest_by_project(db: Session, project_id: uuid.UUID) -> ConfidenceScore | None:
    return (
        db.query(ConfidenceScore)
        .filter(ConfidenceScore.project_id == project_id)
        .order_by(ConfidenceScore.calculated_at.desc())
        .first()
    )


def delete_by_project(db: Session, project_id: uuid.UUID) -> None:
    db.query(ConfidenceScore).filter(ConfidenceScore.project_id == project_id).delete()
    db.flush()
