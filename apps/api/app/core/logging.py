# Structured logging setup.
# Call setup_logging() once at application startup (in main.py lifespan).
# Use get_logger(__name__) in any module to get a named logger.
import logging
import sys

from app.config import settings


def setup_logging() -> None:
    level = logging.DEBUG if settings.app_env in ("local", "test") else logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
