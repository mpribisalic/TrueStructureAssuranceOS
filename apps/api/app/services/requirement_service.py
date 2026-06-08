import uuid

from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.core.errors import ConflictError, NotFoundError
from app.models.requirement import HumanReviewStatus, Requirement, RequirementStatus
from app.repositories import document_repo, requirement_repo
from app.schemas.requirement import RequirementCreate, RequirementUpdate


def extract_requirements(db: Session, document_id: uuid.UUID) -> list[Requirement]:
    doc = document_repo.get_by_id(db, document_id)
    if not doc:
        raise NotFoundError("Document not found")
    if not doc.extracted_text:
        raise NotFoundError("Document has no extracted text — process it first")

    ai = get_ai_provider()
    result = ai.extract_requirements(doc.extracted_text)

    created: list[Requirement] = []
    for extracted in result.requirements:
        existing = requirement_repo.get_by_external_id(db, doc.project_id, extracted.external_id)
        if existing:
            continue
        req = Requirement(
            project_id=doc.project_id,
            source_document_id=doc.id,
            external_id=extracted.external_id,
            title=extracted.title,
            text=extracted.text,
            category=extracted.category,
            criticality=extracted.criticality,
            priority="medium",
            verification_method=extracted.verification_method,
            status=RequirementStatus.active,
            ai_confidence=extracted.confidence,
            source_reference=extracted.source_reference,
            human_review_status=HumanReviewStatus.pending,
        )
        requirement_repo.create(db, req)
        created.append(req)

    db.flush()
    return created


def list_requirements(db: Session, project_id: uuid.UUID) -> list[Requirement]:
    return requirement_repo.get_all(db, project_id)


def create_requirement(
    db: Session, project_id: uuid.UUID, payload: RequirementCreate
) -> Requirement:
    existing = requirement_repo.get_by_external_id(db, project_id, payload.external_id)
    if existing:
        raise ConflictError(f"Requirement {payload.external_id} already exists")
    req = Requirement(
        project_id=project_id,
        external_id=payload.external_id,
        title=payload.title,
        text=payload.text,
        category=payload.category,
        criticality=payload.criticality,
        priority=payload.priority,
        verification_method=payload.verification_method,
        status=RequirementStatus.active,
        human_review_status=HumanReviewStatus.pending,
    )
    requirement_repo.create(db, req)
    db.flush()
    return req


def get_requirement(db: Session, requirement_id: uuid.UUID) -> Requirement:
    req = requirement_repo.get_by_id(db, requirement_id)
    if not req:
        raise NotFoundError("Requirement not found")
    return req


def update_requirement(
    db: Session, requirement_id: uuid.UUID, payload: RequirementUpdate
) -> Requirement:
    req = get_requirement(db, requirement_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(req, field, value)
    db.flush()
    return req


def approve_requirement(db: Session, requirement_id: uuid.UUID) -> Requirement:
    req = get_requirement(db, requirement_id)
    req.human_review_status = HumanReviewStatus.approved
    db.flush()
    return req


def reject_requirement(db: Session, requirement_id: uuid.UUID) -> Requirement:
    req = get_requirement(db, requirement_id)
    req.human_review_status = HumanReviewStatus.rejected
    db.flush()
    return req
