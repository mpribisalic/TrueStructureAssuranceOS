import uuid

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.core.logging import get_logger
from app.documents.extractor import extract_text, get_extension
from app.documents.validator import compute_hash, validate_upload
from app.models.document import Document, DocumentSourceType, ProcessingStatus
from app.models.user import User
from app.repositories import document_repo
from app.storage.factory import get_storage

logger = get_logger(__name__)


def upload_document(
    db: Session,
    project_id: uuid.UUID,
    filename: str,
    data: bytes,
    source_type: DocumentSourceType,
    user: User,
) -> Document:
    validate_upload(filename, data)

    file_hash = compute_hash(data)
    storage_key = f"projects/{project_id}/documents/{file_hash}/{filename}"

    storage = get_storage()
    storage_uri = storage.upload(storage_key, data)

    document = Document(
        project_id=project_id,
        uploaded_by_user_id=user.id,
        filename=filename,
        file_type=get_extension(filename),
        source_type=source_type,
        storage_uri=storage_uri,
        file_hash=file_hash,
        file_size_bytes=len(data),
        processing_status=ProcessingStatus.pending,
    )
    document_repo.create(db, document)

    # Extract text synchronously for now (background jobs added in later phase)
    _process_document(db, document, data)
    return document


def _process_document(db: Session, document: Document, data: bytes) -> None:
    document.processing_status = ProcessingStatus.processing
    db.flush()
    try:
        document.extracted_text = extract_text(document.filename, data)
        document.processing_status = ProcessingStatus.done
    except Exception as exc:
        logger.warning("Text extraction failed for %s: %s", document.filename, exc)
        document.processing_error = str(exc)
        document.processing_status = ProcessingStatus.failed
    db.flush()


def list_documents(db: Session, project_id: uuid.UUID) -> list[Document]:
    return document_repo.get_all(db, project_id)


def get_document(db: Session, document_id: uuid.UUID) -> Document:
    doc = document_repo.get_by_id(db, document_id)
    if not doc:
        raise NotFoundError("Document not found")
    return doc


def reprocess_document(db: Session, document_id: uuid.UUID) -> Document:
    """Re-run text extraction using stored file bytes."""
    document = get_document(db, document_id)
    if not document.storage_uri:
        raise NotFoundError("Document has no stored file")
    storage_key = document.storage_uri.split("://", 1)[-1].lstrip("/")
    # MinIO URIs are bucket/key — strip bucket prefix
    if "/" in storage_key and not storage_key.startswith("projects/"):
        storage_key = storage_key.split("/", 1)[1]
    data = get_storage().download(storage_key)
    _process_document(db, document, data)
    return document
