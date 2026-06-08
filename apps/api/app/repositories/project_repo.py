import uuid

from sqlalchemy.orm import Session

from app.models.project import Project, ProjectStatus


def get_all(db: Session, organization_id: uuid.UUID) -> list[Project]:
    return (
        db.query(Project)
        .filter(Project.organization_id == organization_id, Project.status != ProjectStatus.archived)
        .order_by(Project.updated_at.desc())
        .all()
    )


def get_by_id(db: Session, project_id: uuid.UUID, organization_id: uuid.UUID) -> Project | None:
    return (
        db.query(Project)
        .filter(Project.id == project_id, Project.organization_id == organization_id)
        .first()
    )


def create(db: Session, project: Project) -> Project:
    db.add(project)
    db.flush()
    return project


def delete(db: Session, project: Project) -> None:
    db.delete(project)
    db.flush()
