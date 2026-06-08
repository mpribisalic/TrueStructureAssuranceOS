"""Confidence Engine — answers HOW TRUSTWORTHY is the readiness score?

Produces a ConfidenceLevel (Low/Medium/High/Very High) plus a numeric score
and a human-readable explanation based on approval ratios across traceability
links, requirements, evidence, and open gaps.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.confidence_score import ConfidenceLevel, ConfidenceScore
from app.models.requirement import HumanReviewStatus
from app.models.gap import GapStatus
from app.models.test_run import TestRunStatus
from app.repositories import confidence_score_repo
from app.repositories.gap_repo import get_all as get_all_gaps
from app.repositories.requirement_repo import get_all as get_all_requirements
from app.repositories.trace_link_repo import get_all as get_all_links
from app.schemas.confidence_score import ConfidenceScoreRead


def calculate_confidence(db: Session, project_id: uuid.UUID) -> ConfidenceScoreRead:
    all_links = get_all_links(db, project_id)
    all_requirements = get_all_requirements(db, project_id)
    all_gaps = get_all_gaps(db, project_id)

    # Test runs for evidence ratio
    from app.models.test_run import TestRun
    test_runs = db.query(TestRun).filter(TestRun.project_id == project_id).all()

    # ── Traceability ratios ───────────────────────────────────────────────────
    total_links = len(all_links)
    approved_links = sum(
        1 for l in all_links if l.human_review_status == HumanReviewStatus.approved
    )
    ai_pending_links = sum(
        1 for l in all_links
        if l.created_by == "ai" and l.human_review_status == HumanReviewStatus.pending
    )

    approved_traceability_ratio = approved_links / total_links if total_links > 0 else 1.0
    ai_only_decisions_ratio = ai_pending_links / total_links if total_links > 0 else 0.0

    # ── Requirements ratio ───────────────────────────────────────────────────
    total_reqs = len(all_requirements)
    approved_reqs = sum(
        1 for r in all_requirements if r.human_review_status == HumanReviewStatus.approved
    )
    approved_requirements_ratio = approved_reqs / total_reqs if total_reqs > 0 else 1.0

    # ── Evidence ratio ───────────────────────────────────────────────────────
    # Test runs with status != pending are considered reviewed evidence
    total_runs = len(test_runs)
    reviewed_runs = sum(
        1 for r in test_runs if r.status != TestRunStatus.pending
    ) if hasattr(TestRunStatus, "pending") else total_runs
    approved_evidence_ratio = reviewed_runs / total_runs if total_runs > 0 else 1.0

    # ── Gaps ratio ────────────────────────────────────────────────────────────
    total_gaps = len(all_gaps)
    open_gaps_count = sum(1 for g in all_gaps if g.status == GapStatus.open)
    open_gaps_ratio = open_gaps_count / total_gaps if total_gaps > 0 else 0.0

    # ── Weighted confidence value (0–100) ─────────────────────────────────────
    confidence_value = (
        approved_traceability_ratio * 35
        + approved_requirements_ratio * 25
        + approved_evidence_ratio * 20
        + (1 - ai_only_decisions_ratio) * 15
        + (1 - open_gaps_ratio) * 5
    )
    confidence_value = round(min(max(confidence_value, 0.0), 100.0), 2)

    # ── Level mapping ─────────────────────────────────────────────────────────
    if confidence_value >= 85:
        level = ConfidenceLevel.very_high
    elif confidence_value >= 65:
        level = ConfidenceLevel.high
    elif confidence_value >= 40:
        level = ConfidenceLevel.medium
    else:
        level = ConfidenceLevel.low

    # ── Explanation ───────────────────────────────────────────────────────────
    weaknesses = []
    if approved_traceability_ratio < 0.7:
        pct = int((1 - approved_traceability_ratio) * 100)
        weaknesses.append(f"{pct}% of traceability links are not yet approved")
    if approved_requirements_ratio < 0.7:
        pct = int((1 - approved_requirements_ratio) * 100)
        weaknesses.append(f"{pct}% of requirements are pending human approval")
    if ai_only_decisions_ratio > 0.2:
        pct = int(ai_only_decisions_ratio * 100)
        weaknesses.append(f"{pct}% of traceability is AI-generated and unreviewed")
    if open_gaps_ratio > 0.5:
        weaknesses.append(f"{open_gaps_count} open gaps remain unresolved")

    if weaknesses:
        explanation = "Confidence reduced: " + "; ".join(weaknesses) + "."
    else:
        explanation = (
            "Confidence is high — traceability, requirements, and evidence are well-reviewed."
        )

    # ── Persist (replace previous score) ─────────────────────────────────────
    confidence_score_repo.delete_by_project(db, project_id)

    score = ConfidenceScore(
        project_id=project_id,
        confidence_level=level,
        confidence_value=confidence_value,
        approved_traceability_ratio=round(approved_traceability_ratio, 4),
        approved_requirements_ratio=round(approved_requirements_ratio, 4),
        approved_evidence_ratio=round(approved_evidence_ratio, 4),
        ai_only_decisions_ratio=round(ai_only_decisions_ratio, 4),
        open_gaps_ratio=round(open_gaps_ratio, 4),
        explanation=explanation,
        calculated_at=datetime.now(timezone.utc),
    )
    confidence_score_repo.create(db, score)
    db.flush()

    return ConfidenceScoreRead.model_validate(score)


def get_latest(db: Session, project_id: uuid.UUID) -> ConfidenceScoreRead:
    score = confidence_score_repo.get_latest_by_project(db, project_id)
    if not score:
        raise NotFoundError("No confidence score calculated yet for this project")
    return ConfidenceScoreRead.model_validate(score)
