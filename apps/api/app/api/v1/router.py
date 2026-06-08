# Central router — import and include all endpoint routers here.
# Each new phase adds its router to this file.
from fastapi import APIRouter

from app.api.v1.endpoints import auth, documents, evidence, gaps, projects, readiness, reports, requirements, test_cases, trace_links
from app.api.v1.endpoints.mission_impact import router as mission_impact_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(projects.router)
router.include_router(documents.router)
router.include_router(requirements.router)
router.include_router(test_cases.router)
router.include_router(evidence.router)
router.include_router(trace_links.router)
router.include_router(gaps.router)
router.include_router(readiness.router)
router.include_router(reports.router)
router.include_router(mission_impact_router, tags=["mission-impact"])
