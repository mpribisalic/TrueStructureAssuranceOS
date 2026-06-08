"""Readiness scoring engine — weighted formula + score caps (section 23 of build spec).

Scores are computed deterministically from current project data. Each call
creates an immutable snapshot so history is preserved.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.gap import GapSeverity, GapStatus
from app.models.readiness import ReadinessScore
from app.models.requirement import HumanReviewStatus, RequirementCriticality
from app.models.test_run import TestRunStatus
from app.models.trace_link import TraceLink
from app.repositories import readiness_repo
from app.repositories.evidence_repo import get_evidence_all
from app.repositories.gap_repo import get_all as get_all_gaps
from app.repositories.requirement_repo import get_all as get_all_requirements
from app.repositories.test_case_repo import get_all as get_all_test_cases
from app.repositories.trace_link_repo import get_all as get_all_links

# Stale-evidence thresholds (days) per criticality — mirrors gap_service
_STALE_DAYS = {
    RequirementCriticality.low: 365,
    RequirementCriticality.medium: 180,
    RequirementCriticality.high: 90,
    RequirementCriticality.critical: 30,
    RequirementCriticality.catastrophic: 30,
}

# Weighted formula weights
_W_COVERAGE = 0.30
_W_PASS = 0.25
_W_EVIDENCE = 0.20
_W_RISK = 0.10
_W_FRESHNESS = 0.10
_W_HUMAN = 0.05


def calculate(db: Session, project_id: uuid.UUID) -> ReadinessScore:
    requirements = get_all_requirements(db, project_id)
    test_cases = {tc.id: tc for tc in get_all_test_cases(db, project_id)}
    all_links = get_all_links(db, project_id)
    all_evidence = get_evidence_all(db, project_id)
    all_gaps = get_all_gaps(db, project_id)

    # Test runs indexed by test_case_id
    from app.models.test_run import TestRun
    test_runs = db.query(TestRun).filter(TestRun.project_id == project_id).all()
    runs_by_tc: dict[uuid.UUID, list[TestRun]] = {}
    for run in test_runs:
        runs_by_tc.setdefault(run.test_case_id, []).append(run)

    # Links indexed by requirement id
    links_by_req: dict[uuid.UUID, list[TraceLink]] = {}
    for link in all_links:
        links_by_req.setdefault(link.source_id, []).append(link)

    now = datetime.now(timezone.utc)
    n_reqs = len(requirements)

    # ── Component scores (0–100) ─────────────────────────────────────────────

    # coverage_score: % requirements with at least one approved test link
    reqs_with_approved_test = 0
    reqs_without_test: list = []
    for req in requirements:
        approved = [
            l for l in links_by_req.get(req.id, [])
            if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
        ]
        if approved:
            reqs_with_approved_test += 1
        else:
            reqs_without_test.append(req)

    coverage_score = (reqs_with_approved_test / n_reqs * 100) if n_reqs else 0.0

    # test_pass_score: % of test runs that passed
    all_runs = test_runs
    passed_runs = [r for r in all_runs if r.status == TestRunStatus.passed]
    test_pass_score = (len(passed_runs) / len(all_runs) * 100) if all_runs else 0.0

    # evidence_score: % requirements with at least one evidence item via linked test runs
    reqs_with_evidence = 0
    reqs_without_evidence: list = []
    for req in requirements:
        approved_tc_ids = {
            l.target_id for l in links_by_req.get(req.id, [])
            if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
        }
        has_ev = any(runs_by_tc.get(tc_id) for tc_id in approved_tc_ids)
        if has_ev:
            reqs_with_evidence += 1
        else:
            reqs_without_evidence.append(req)

    evidence_score = (reqs_with_evidence / n_reqs * 100) if n_reqs else 0.0

    # risk_score: based on open gap severity distribution (fewer/lighter gaps = higher score)
    open_gaps = [g for g in all_gaps if g.status == GapStatus.open]
    critical_gaps = sum(1 for g in open_gaps if g.severity == GapSeverity.critical)
    high_gaps = sum(1 for g in open_gaps if g.severity == GapSeverity.high)
    medium_gaps = sum(1 for g in open_gaps if g.severity == GapSeverity.medium)
    low_gaps = sum(1 for g in open_gaps if g.severity == GapSeverity.low)
    gap_penalty = critical_gaps * 20 + high_gaps * 10 + medium_gaps * 5 + low_gaps * 2
    risk_score = max(0.0, 100.0 - gap_penalty)

    # freshness_score: % of requirements whose evidence is within the staleness threshold
    fresh_reqs = 0
    for req in requirements:
        threshold = _STALE_DAYS.get(req.criticality, 180)
        approved_tc_ids = {
            l.target_id for l in links_by_req.get(req.id, [])
            if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
        }
        linked_runs = [r for tc_id in approved_tc_ids for r in runs_by_tc.get(tc_id, [])]
        if not linked_runs:
            continue
        most_recent = max(
            (r.executed_at if r.executed_at.tzinfo else r.executed_at.replace(tzinfo=timezone.utc))
            for r in linked_runs
        )
        if (now - most_recent).days <= threshold:
            fresh_reqs += 1

    freshness_score = (fresh_reqs / n_reqs * 100) if n_reqs else 0.0

    # human_review_score: % of AI-suggested links that have been reviewed (approved or rejected)
    ai_links = [l for l in all_links if l.created_by == "ai"]
    reviewed_ai = [
        l for l in ai_links
        if l.human_review_status in (HumanReviewStatus.approved, HumanReviewStatus.rejected)
    ]
    human_review_score = (len(reviewed_ai) / len(ai_links) * 100) if ai_links else 100.0

    # ── Weighted sum ─────────────────────────────────────────────────────────
    raw_score = (
        _W_COVERAGE * coverage_score
        + _W_PASS * test_pass_score
        + _W_EVIDENCE * evidence_score
        + _W_RISK * risk_score
        + _W_FRESHNESS * freshness_score
        + _W_HUMAN * human_review_score
    )

    # ── Score caps ───────────────────────────────────────────────────────────
    caps_applied: list[str] = []
    cap = 100.0

    if not all_evidence:
        cap = min(cap, 49.0)
        caps_applied.append("No evidence exists — max 49")

    for req in requirements:
        if req.criticality == RequirementCriticality.catastrophic:
            approved = [
                l for l in links_by_req.get(req.id, [])
                if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
            ]
            if not approved:
                cap = min(cap, 59.0)
                caps_applied.append(f"Catastrophic requirement {req.external_id} has no approved test — max 59")
                break

    for req in requirements:
        if req.criticality in (RequirementCriticality.critical, RequirementCriticality.catastrophic):
            if req.category == "safety":
                approved_tc_ids = {
                    l.target_id for l in links_by_req.get(req.id, [])
                    if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
                }
                has_ev = any(runs_by_tc.get(tc_id) for tc_id in approved_tc_ids)
                if not has_ev:
                    cap = min(cap, 69.0)
                    caps_applied.append(f"Critical safety requirement {req.external_id} has no evidence — max 69")
                    break

    for req in requirements:
        if req.criticality in (RequirementCriticality.critical, RequirementCriticality.catastrophic):
            if req.category == "security":
                approved_tc_ids = {
                    l.target_id for l in links_by_req.get(req.id, [])
                    if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
                }
                has_ev = any(runs_by_tc.get(tc_id) for tc_id in approved_tc_ids)
                if not has_ev:
                    cap = min(cap, 69.0)
                    caps_applied.append(f"Critical security requirement {req.external_id} has no evidence — max 69")
                    break

    for tc_id, runs in runs_by_tc.items():
        tc = test_cases.get(tc_id)
        # Check if this TC is linked to any critical requirement
        for req in requirements:
            if req.criticality in (RequirementCriticality.critical, RequirementCriticality.catastrophic):
                approved_tc_ids = {
                    l.target_id for l in links_by_req.get(req.id, [])
                    if l.target_type == "test_case" and l.human_review_status == HumanReviewStatus.approved
                }
                if tc_id in approved_tc_ids:
                    if any(r.status == TestRunStatus.failed for r in runs):
                        cap = min(cap, 74.0)
                        caps_applied.append(f"Critical linked test {tc.external_id if tc else tc_id} failed — max 74")

    if n_reqs and len(reqs_without_test) / n_reqs > 0.30:
        cap = min(cap, 79.0)
        pct = round(len(reqs_without_test) / n_reqs * 100)
        caps_applied.append(f"{pct}% of requirements lack tests (>30%) — max 79")

    if ai_links and not reviewed_ai:
        cap = min(cap, 69.0)
        caps_applied.append("All AI trace links are unreviewed — max 69")

    overall_score = round(min(raw_score, cap), 1)

    # ── Top blockers & recommended actions ───────────────────────────────────
    top_blockers: list[str] = []
    for gap in sorted(open_gaps, key=lambda g: (g.severity.value, str(g.gap_type)), reverse=True)[:5]:
        top_blockers.append(gap.title)

    recommended_actions: list[str] = []
    if reqs_without_test:
        recommended_actions.append(
            f"Add test cases and approve trace links for {len(reqs_without_test)} uncovered requirement(s)."
        )
    if reqs_without_evidence:
        recommended_actions.append(
            f"Import evidence for {len(reqs_without_evidence)} requirement(s) that lack test run records."
        )
    failed_count = len(all_runs) - len(passed_runs)
    if failed_count:
        recommended_actions.append(f"Investigate and re-run {failed_count} failed test(s).")
    unreviewed_ai = len(ai_links) - len(reviewed_ai)
    if unreviewed_ai:
        recommended_actions.append(f"Review {unreviewed_ai} pending AI-suggested trace link(s).")

    explanation = (
        f"Readiness score {overall_score}/100 based on: "
        f"coverage {coverage_score:.0f}%, "
        f"test pass rate {test_pass_score:.0f}%, "
        f"evidence {evidence_score:.0f}%, "
        f"risk {risk_score:.0f}%, "
        f"freshness {freshness_score:.0f}%, "
        f"human review {human_review_score:.0f}%."
    )
    if caps_applied:
        explanation += f" Score capped at {cap:.0f} due to: {'; '.join(caps_applied[:2])}."

    score = ReadinessScore(
        project_id=project_id,
        overall_score=overall_score,
        coverage_score=round(coverage_score, 1),
        test_pass_score=round(test_pass_score, 1),
        evidence_score=round(evidence_score, 1),
        risk_score=round(risk_score, 1),
        freshness_score=round(freshness_score, 1),
        human_review_score=round(human_review_score, 1),
        critical_blocker_count=critical_gaps,
        high_gap_count=high_gaps,
        medium_gap_count=medium_gaps,
        low_gap_count=low_gaps,
        explanation=explanation,
        caps_applied_json=caps_applied,
        top_blockers_json=top_blockers,
        recommended_actions_json=recommended_actions,
    )
    readiness_repo.create(db, score)
    db.flush()
    return score


def get_latest(db: Session, project_id: uuid.UUID) -> ReadinessScore:
    score = readiness_repo.get_latest(db, project_id)
    if not score:
        raise NotFoundError("No readiness score calculated yet for this project")
    return score


def get_history(db: Session, project_id: uuid.UUID) -> list[ReadinessScore]:
    return readiness_repo.get_history(db, project_id)
