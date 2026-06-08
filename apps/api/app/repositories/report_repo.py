import uuid

from sqlalchemy.orm import Session

from app.models.report import Report


def create(db: Session, report: Report) -> Report:
    db.add(report)
    db.flush()
    return report


def get_all(db: Session, project_id: uuid.UUID) -> list[Report]:
    return (
        db.query(Report)
        .filter(Report.project_id == project_id)
        .order_by(Report.created_at.desc())
        .all()
    )


def get_by_id(db: Session, report_id: uuid.UUID) -> Report | None:
    return db.get(Report, report_id)
