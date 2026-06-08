"""Standards mapping framework — coming in Phase 17 (post-TRL4)."""
import uuid
from typing import List

from fastapi import APIRouter

from app.core.deps import RequireEngineer
from app.schemas.standards import StandardCoverageResponse, StandardRead

router = APIRouter(tags=["standards"])


@router.get("/standards", response_model=List[StandardRead])
def list_standards(
    current_user: RequireEngineer,
) -> List[StandardRead]:
    """List all standards. Stub — returns empty list until post-TRL4 implementation."""
    return []


@router.get(
    "/projects/{project_id}/standards/coverage",
    response_model=StandardCoverageResponse,
)
def get_standards_coverage(
    project_id: uuid.UUID,
    current_user: RequireEngineer,
) -> StandardCoverageResponse:
    """Return standards coverage for a project. Stub placeholder."""
    return StandardCoverageResponse(
        standard_id=None,
        standard_name="STANAG (stub)",
        total_clauses=0,
        covered_clauses=0,
        coverage_percent=0.0,
        missing_clauses=[],
        note="Standards mapping available post-TRL4 deployment",
    )
