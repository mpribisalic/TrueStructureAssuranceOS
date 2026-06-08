import os
from pathlib import Path

from app.storage.base import StorageBackend

# Default local storage directory — created automatically if missing
LOCAL_STORAGE_DIR = Path(os.getenv("LOCAL_STORAGE_DIR", "/tmp/assurance_os_storage"))


class LocalStorage(StorageBackend):
    """File system storage for local dev and test environments."""

    def __init__(self, base_dir: Path = LOCAL_STORAGE_DIR) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        path = self.base_dir / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return f"local://{key}"

    def download(self, key: str) -> bytes:
        path = self.base_dir / key
        if not path.exists():
            raise FileNotFoundError(f"Storage object not found: {key}")
        return path.read_bytes()

    def delete(self, key: str) -> None:
        path = self.base_dir / key
        if path.exists():
            path.unlink()
