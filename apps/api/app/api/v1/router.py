# Central router — import and include all endpoint routers here.
# Each new phase adds its router to this file.
from fastapi import APIRouter

from app.api.v1.endpoints import auth, documents, evidence, projects, requirements, test_cases

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(projects.router)
router.include_router(documents.router)
router.include_router(requirements.router)
router.include_router(test_cases.router)
router.include_router(evidence.router)
