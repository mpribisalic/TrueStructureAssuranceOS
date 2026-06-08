"""Traceability link service: AI-assisted suggestions + human approve/reject."""
import uuid

from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.core.errors import NotFoundError
from app.models.requirement import HumanReviewStatus
from app.models.trace_link import TraceLink
from app.repositories import trace_link_repo
from app.repositories.requirement_repo import get_all as get_all_requirements
from app.repositories.test_case_repo import get_all as get_all_test_cases
from app.repositories.test_case_repo import get_by_external_id as get_tc_by_ext
from app.schemas.trace_link import TraceLinkSuggestResult


def suggest_links(db: Session, project_id: uuid.UUID) -> TraceLinkSuggestResult:
    requirements = get_all_requirements(db, project_id)
    test_cases = get_all_test_cases(db, project_id)

    ai = get_ai_provider()
    result = ai.suggest_trace_links(requirements, test_cases, evidence=[])

    created: list[TraceLink] = []
    skipped = 0

    # Build a lookup from external_id → TestCase
    tc_by_ext: dict[str, object] = {tc.external_id: tc for tc in test_cases}
    req_by_ext: dict[str, object] = {r.external_id: r for r in requirements}

    for suggestion in result.links:
        req = req_by_ext.get(suggestion.requirement_external_id)
        tc = tc_by_ext.get(suggestion.test_case_external_id)
        if not req or not tc:
            skipped += 1
            continue

        if trace_link_repo.exists(db, project_id, req.id, tc.id, suggestion.link_type):
            skipped += 1
            continue

        link = TraceLink(
            project_id=project_id,
            source_type="requirement",
            source_id=req.id,
            target_type="test_case",
            target_id=tc.id,
            link_type=suggestion.link_type,
            confidence=suggestion.confidence,
            reason=suggestion.reason,
            created_by="ai",
            human_review_status=HumanReviewStatus.pending,
        )
        trace_link_repo.create(db, link)
        created.append(link)

    db.flush()
    return TraceLinkSuggestResult(
        suggested=len(created),
        skipped=skipped,
        links=created,
    )


def create_manual_link(db: Session, project_id: uuid.UUID, payload) -> TraceLink:
    from app.schemas.trace_link import TraceLinkCreate
    if trace_link_repo.exists(db, project_id, payload.source_id, payload.target_id, payload.link_type):
        from app.core.errors import ConflictError
        raise ConflictError("Trace link already exists")
    link = TraceLink(
        project_id=project_id,
        source_type="requirement",
        source_id=payload.source_id,
        target_type=payload.target_type,
        target_id=payload.target_id,
        link_type=payload.link_type,
        created_by="user",
        human_review_status=HumanReviewStatus.approved,
    )
    trace_link_repo.create(db, link)
    db.flush()
    return link


def list_links(db: Session, project_id: uuid.UUID) -> list[TraceLink]:
    return trace_link_repo.get_all(db, project_id)


def _get_link(db: Session, link_id: uuid.UUID) -> TraceLink:
    link = trace_link_repo.get_by_id(db, link_id)
    if not link:
        raise NotFoundError("Trace link not found")
    return link


def approve_link(db: Session, link_id: uuid.UUID) -> TraceLink:
    link = _get_link(db, link_id)
    link.human_review_status = HumanReviewStatus.approved
    db.flush()
    return link


def reject_link(db: Session, link_id: uuid.UUID) -> TraceLink:
    link = _get_link(db, link_id)
    link.human_review_status = HumanReviewStatus.rejected
    db.flush()
    return link
