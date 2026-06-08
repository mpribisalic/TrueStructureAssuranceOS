from functools import lru_cache

from app.config import settings
from app.storage.base import StorageBackend


@lru_cache(maxsize=1)
def get_storage() -> StorageBackend:
    """Returns the configured storage backend. Cached after first call."""
    if settings.object_storage_provider == "minio":
        from app.storage.minio import MinIOStorage
        return MinIOStorage()
    from app.storage.local import LocalStorage
    return LocalStorage()
