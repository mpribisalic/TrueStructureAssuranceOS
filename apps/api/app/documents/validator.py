import hashlib

from app.config import settings
from app.core.errors import ValidationError
from app.documents.extractor import ALLOWED_EXTENSIONS, get_extension


def validate_upload(filename: str, data: bytes) -> None:
    """Raise ValidationError if the file fails any upload check."""
    ext = get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"File type '.{ext}' not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise ValidationError(
            f"File too large ({len(data) // 1024 // 1024} MB). Maximum: {settings.max_upload_size_mb} MB"
        )


def compute_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
