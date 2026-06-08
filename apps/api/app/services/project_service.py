import uuid

from sqlalchemy.orm import Session

from app.core.errors import ForbiddenError, NotFoundError
from app.models.project import Project
from app.models.user import User
from app.repositories import project_repo
from app.schemas.project import ProjectCreate, ProjectUpdate


def list_projects(db: Session, user: User) -> list[Project]:
    return project_repo.get_all(db, user.organization_id)


def get_project(db: Session, project_id: uuid.UUID, user: User) -> Project:
    project = project_repo.get_by_id(db, project_id, user.organization_id)
    if not project:
        raise NotFoundError("Project not found")
    return project


def create_project(db: Session, data: ProjectCreate, user: User) -> Project:
    project = Project(
        organization_id=user.organization_id,
        **data.model_dump(),
    )
    return project_repo.create(db, project)


def update_project(db: Session, project_id: uuid.UUID, data: ProjectUpdate, user: User) -> Project:
    project = get_project(db, project_id, user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.flush()
    return project


def delete_project(db: Session, project_id: uuid.UUID, user: User) -> None:
    from app.models.user import UserRole
    if user.role != UserRole.admin:
        raise ForbiddenError("Only admins can delete projects")
    project = get_project(db, project_id, user)
    project_repo.delete(db, project)
