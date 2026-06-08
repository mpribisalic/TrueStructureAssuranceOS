# Application entry point.
# Routes are registered here as they are implemented in later phases.
# Middleware, exception handlers and lifespan events are also added here.
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import router as api_router
from app.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.db.base import import_all_models
from app.db.session import SessionLocal

# Import all models so SQLAlchemy relationship resolution works at startup
import_all_models()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    setup_logging()
    logger.info("Starting %s [env=%s]", settings.app_name, settings.app_env)
    yield
    logger.info("Shutting down")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Liveness probe — also checks database connectivity."""
    db_ok = False
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        logger.warning("Database health check failed")

    return {
        "status": "ok" if db_ok else "degraded",
        "app": settings.app_name,
        "env": settings.app_env,
        "database": "ok" if db_ok else "unavailable",
    }
