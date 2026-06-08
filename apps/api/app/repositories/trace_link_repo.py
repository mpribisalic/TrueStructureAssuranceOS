import uuid

from sqlalchemy.orm import Session

from app.models.trace_link import TraceLink


def create(db: Session, link: TraceLink) -> TraceLink:
    db.add(link)
    db.flush()
    return link


def get_all(db: Session, project_id: uuid.UUID) -> list[TraceLink]:
    return (
        db.query(TraceLink)
        .filter(TraceLink.project_id == project_id)
        .order_by(TraceLink.created_at.desc())
        .all()
    )


def get_by_id(db: Session, link_id: uuid.UUID) -> TraceLink | None:
    return db.get(TraceLink, link_id)


def exists(
    db: Session,
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    target_id: uuid.UUID,
    link_type: str,
) -> bool:
    return (
        db.query(TraceLink)
        .filter(
            TraceLink.project_id == project_id,
            TraceLink.source_id == source_id,
            TraceLink.target_id == target_id,
            TraceLink.link_type == link_type,
        )
        .first()
    ) is not None
