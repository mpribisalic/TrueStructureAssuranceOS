import uuid

from sqlalchemy.orm import Session

from app.models.document import Document


def get_all(db: Session, project_id: uuid.UUID) -> list[Document]:
    return (
        db.query(Document)
        .filter(Document.project_id == project_id)
        .order_by(Document.created_at.desc())
        .all()
    )


def get_by_id(db: Session, document_id: uuid.UUID) -> Document | None:
    return db.get(Document, document_id)


def create(db: Session, document: Document) -> Document:
    db.add(document)
    db.flush()
    return document
