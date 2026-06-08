# Storage abstraction — all file operations go through this interface.
# LocalStorage is used in local/test environments.
# MinIOStorage is used when OBJECT_STORAGE_PROVIDER=minio (Docker deployment).
# New providers (S3, Azure Blob) can be added without changing service code.
import abc


class StorageBackend(abc.ABC):
    @abc.abstractmethod
    def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        """Upload bytes and return the storage URI."""

    @abc.abstractmethod
    def download(self, key: str) -> bytes:
        """Download and return raw bytes."""

    @abc.abstractmethod
    def delete(self, key: str) -> None:
        """Delete an object."""
