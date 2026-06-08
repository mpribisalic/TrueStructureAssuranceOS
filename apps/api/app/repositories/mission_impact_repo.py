import uuid

from sqlalchemy.orm import Session

from app.models.mission_impact import MissionImpact


def create(db: Session, impact: MissionImpact) -> MissionImpact:
    db.add(impact)
    db.flush()
    return impact


def get_by_project(db: Session, project_id: uuid.UUID) -> list[MissionImpact]:
    return (
        db.query(MissionImpact)
        .filter(MissionImpact.project_id == project_id)
        .order_by(MissionImpact.created_at.desc())
        .all()
    )


def delete_by_project(db: Session, project_id: uuid.UUID) -> None:
    db.query(MissionImpact).filter(MissionImpact.project_id == project_id).delete()
    db.flush()
