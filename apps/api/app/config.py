# All configuration is loaded from environment variables.
# Never add secrets or defaults with real values here — use .env.example as the template.
# pydantic-settings reads from the .env file automatically when present.
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    app_name: str = "True Structure Assurance OS"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "postgresql+psycopg://assurance_user:assurance_pass@localhost:5432/assurance_os"
    redis_url: str = "redis://localhost:6379/0"

    object_storage_provider: str = "minio"
    object_storage_endpoint: str = "http://localhost:9000"
    object_storage_bucket: str = "assurance-os"
    object_storage_access_key: str = "minio"
    object_storage_secret_key: str = "minio123"
    object_storage_region: str = "local"

    llm_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"

    jwt_secret: str = "change-this-in-production"
    jwt_expires_minutes: int = 1440

    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("database_url", mode="before")
    @classmethod
    def fix_postgres_url(cls, v: str) -> str:
        # Railway provides postgresql:// but psycopg3 needs postgresql+psycopg://
        if v and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

    max_upload_size_mb: int = 25
    enable_ai: bool = True
    enable_signups: bool = False


settings = Settings()
