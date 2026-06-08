import boto3
from botocore.client import Config

from app.config import settings
from app.storage.base import StorageBackend


class MinIOStorage(StorageBackend):
    """S3-compatible storage backed by MinIO (used in Docker deployment)."""

    def __init__(self) -> None:
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.object_storage_endpoint,
            aws_access_key_id=settings.object_storage_access_key,
            aws_secret_access_key=settings.object_storage_secret_key,
            region_name=settings.object_storage_region,
            config=Config(signature_version="s3v4"),
        )
        self._bucket = settings.object_storage_bucket
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        try:
            self._client.head_bucket(Bucket=self._bucket)
        except Exception:
            self._client.create_bucket(Bucket=self._bucket)

    def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        self._client.put_object(
            Bucket=self._bucket, Key=key, Body=data, ContentType=content_type
        )
        return f"minio://{self._bucket}/{key}"

    def download(self, key: str) -> bytes:
        response = self._client.get_object(Bucket=self._bucket, Key=key)
        return response["Body"].read()

    def delete(self, key: str) -> None:
        self._client.delete_object(Bucket=self._bucket, Key=key)
