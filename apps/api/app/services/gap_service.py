"""Deterministic gap detection — 7 rules as specified in section 22 of the build spec.

Each run clears existing open gaps and re-evaluates from scratch so the
result always reflects the current project state.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.gap import Gap, GapSeverity, GapStatus, GapType
from app.models.requirement import HumanReviewStatus, RequirementCriticality
from app.models.test_run import TestRunStatus
from app.models.trace_link import TraceLink
from app.repositories import gap_repo
from app.repositories.evidence_repo import get_evidence_all
from app.repositories.requirement_repo import get_all as get_all_requirements
from app.repositories.test_case_repo import get_all as get_all_test_cases
from app.repositories.trace_link_repo import get_all as get_all_links
from app.schemas.gap import GapDetectResult, GapUpdate

# Stale-evidence thresholds per criticality level (days)
_STALE_DAYS = {
    RequirementCriticality.low: 365,
    RequirementCriticality.medium: 180,
    RequirementCriticality.high: 90,
    RequirementCriticality.critical: 30,
    RequirementCriticality.catastrophic: 30,
}

_SAFETY_TEST_TYPES = {"safety", "system", "simulation"}
_SECURITY_TEST_TYPES = {"security"}


def _severity_from_criticality(criticality: RequirementCriticality) -> GapSeverity:
    if criticality in (RequirementCriticality.catastrophic, RequirementCriticality.critical):
        return GapSeverity.critical
    if criticality == RequirementCriticality.high:
        return GapSeverity.high
    if criticality == RequirementCriticality.medium:
        return GapSeverity.medium
    return GapSeverity.low


def detect_gaps(db: Session, project_id: uuid.UUID) -> GapDetectResult:
    # Clear previous open gaps so each run is authoritative
    gap_repo.delete_all(db, project_id)

    requirements = get_all_requirements(db, project_id)
    test_cases = {tc.id: tc for tc in get_all_test_cases(db, project_id)}
    all_links = get_all_links(db, project_id)
    all_evidence = get_evidence_all(db, project_id)

    # Pre-index links by source requirement
    links_by_req: dict[uuid.UUID, list[TraceLink]] = {}
    for link in all_links:
        links_by_req.setdefault(link.source_id, []).append(link)

    # Pre-index evidence by test_run_id and test_case via trace links
    evidence_by_test_run: dict[uuid.UUID, list] = {}
    for ev in all_evidence:
        if ev.test_run_id:
            evidence_by_test_run.setdefault(ev.test_run_id, []).append(ev)

    # Build test run lookup from test_case_id → list of test runs
    from app.models.test_run import TestRun
    test_runs = db.query(TestRun).filter(TestRun.project_id == project_id).all()
    runs_by_tc: dict[uuid.UUID, list[TestRun]] = {}
    for run in test_runs:
        runs_by_tc.setdefault(run.test_case_id, []).append(run)

    now = datetime.now(timezone.utc)
    created: list[Gap] = []

    for req in requirements:
        req_links = links_by_req.get(req.id, [])
        approved_links = [l for l in req_links if l.human_review_status == HumanReviewStatus.approved]
        tc_links = [l for l in req_links if l.target_type == "test_case"]
        approved_tc_links = [l for l in tc_links if l.human_review_status == HumanReviewStatus.approved]

        # Pre-compute for Rule 1 vs Rule 7 disambiguation
        pending_ai_links = [
            l for l in tc_links
            if l.created_by == "ai" and l.human_review_status == HumanReviewStatus.pending
        ]
        manual_or_approved_links = [
            l for l in tc_links
            if l.created_by != "ai" or l.human_review_status == HumanReviewStatus.approved
        ]

        # Rule 1 / Rule 7: no approved trace link to any test case
        if not approved_tc_links:
            if pending_ai_links and not manual_or_approved_links:
                # Rule 7: pending AI suggestions exist but none approved yet
                g = _make_gap(
                    project_id, GapType.unapproved_ai_suggestion,
                    f"Unapproved AI suggestions only for {req.external_id}",
                    f"Requirement {req.external_id} has only unapproved AI-suggested trace links. Human review is required.",
                    GapSeverity.medium,
                    req_id=req.id,
                    recommendation="Review and approve or reject the AI-suggested trace links.",
                )
            else:
                # Rule 1: no links at all
                g = _make_gap(
                    project_id, GapType.missing_test,
                    f"No approved test for {req.external_id}",
                    f"Requirement {req.external_id} has no approved traceability link to a test case.",
                    _severity_from_criticality(req.criticality),
                    req_id=req.id,
                    recommendation="Add a test case and approve the trace link.",
                )
            gap_repo.create(db, g)
            created.append(g)
            # Rules 2-6 require an approved test link — skip for this requirement
            continue

        # Gather test cases this requirement is approved-linked to
        linked_tc_ids = {l.target_id for l in approved_tc_links}
        linked_tcs = [test_cases[tc_id] for tc_id in linked_tc_ids if tc_id in test_cases]

        # Collect all runs for linked test cases
        linked_runs: list = []
        for tc in linked_tcs:
            linked_runs.extend(runs_by_tc.get(tc.id, []))

        # Rule 2: approved test link exists but no evidence / test run
        if not linked_runs:
            g = _make_gap(
                project_id, GapType.missing_evidence,
                f"No evidence for {req.external_id}",
                f"Requirement {req.external_id} has approved test links but no test runs or evidence.",
                _severity_from_criticality(req.criticality),
                req_id=req.id,
                recommendation="Import evidence records for the linked test cases.",
            )
            gap_repo.create(db, g)
            created.append(g)

        # Rule 3: any linked test run failed
        for run in linked_runs:
            if run.status == TestRunStatus.failed:
                tc = test_cases.get(run.test_case_id)
                g = _make_gap(
                    project_id, GapType.failed_test,
                    f"Failed test run for {req.external_id}",
                    f"A test run for {req.external_id} (test case {tc.external_id if tc else run.test_case_id}) failed.",
                    GapSeverity.critical if req.criticality in (RequirementCriticality.catastrophic, RequirementCriticality.critical) else GapSeverity.high,
                    req_id=req.id,
                    tc_id=run.test_case_id,
                    recommendation="Investigate and re-run the failed test.",
                )
                gap_repo.create(db, g)
                created.append(g)

        # Rule 4: security requirement — no linked security test
        if req.category == "security":
            has_security_test = any(
                tc.test_type in _SECURITY_TEST_TYPES for tc in linked_tcs
            )
            if not has_security_test:
                g = _make_gap(
                    project_id, GapType.missing_security_validation,
                    f"No security test for {req.external_id}",
                    f"Security requirement {req.external_id} has no linked security-type test case.",
                    GapSeverity.critical,
                    req_id=req.id,
                    recommendation="Add a security test case and link it to this requirement.",
                )
                gap_repo.create(db, g)
                created.append(g)

        # Rule 5: safety requirement — no linked safety/system/simulation test
        if req.category == "safety":
            has_safety_test = any(
                tc.test_type in _SAFETY_TEST_TYPES for tc in linked_tcs
            )
            if not has_safety_test:
                g = _make_gap(
                    project_id, GapType.missing_safety_validation,
                    f"No safety validation test for {req.external_id}",
                    f"Safety requirement {req.external_id} has no linked system/simulation/safety test.",
                    GapSeverity.critical,
                    req_id=req.id,
                    recommendation="Add a system, simulation, or safety test case.",
                )
                gap_repo.create(db, g)
                created.append(g)

        # Rule 6: stale evidence
        threshold_days = _STALE_DAYS.get(req.criticality, 180)
        for run in linked_runs:
            executed = run.executed_at
            if executed.tzinfo is None:
                executed = executed.replace(tzinfo=timezone.utc)
            age_days = (now - executed).days
            if age_days > threshold_days:
                evs = evidence_by_test_run.get(run.id, [])
                ev_id = evs[0].id if evs else None
                g = _make_gap(
                    project_id, GapType.stale_evidence,
                    f"Stale evidence for {req.external_id}",
                    f"Evidence for {req.external_id} is {age_days} days old (threshold: {threshold_days} days for {req.criticality.value} criticality).",
                    _severity_from_criticality(req.criticality),
                    req_id=req.id,
                    evidence_id=ev_id,
                    recommendation=f"Re-run tests and update evidence within the {threshold_days}-day window.",
                )
                gap_repo.create(db, g)
                created.append(g)
                break  # one stale gap per requirement is enough


    db.flush()
    return GapDetectResult(detected=len(created), gaps=created)


def list_gaps(db: Session, project_id: uuid.UUID) -> list[Gap]:
    return gap_repo.get_all(db, project_id)


def update_gap(db: Session, gap_id: uuid.UUID, payload: GapUpdate) -> Gap:
    gap = gap_repo.get_by_id(db, gap_id)
    if not gap:
        raise NotFoundError("Gap not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(gap, field, value)
    db.flush()
    return gap


def _make_gap(
    project_id: uuid.UUID,
    gap_type: GapType,
    title: str,
    description: str,
    severity: GapSeverity,
    req_id: uuid.UUID | None = None,
    tc_id: uuid.UUID | None = None,
    evidence_id: uuid.UUID | None = None,
    recommendation: str | None = None,
) -> Gap:
    return Gap(
        project_id=project_id,
        gap_type=gap_type,
        title=title,
        description=description,
        severity=severity,
        status=GapStatus.open,
        related_requirement_id=req_id,
        related_test_case_id=tc_id,
        related_evidence_id=evidence_id,
        recommendation=recommendation,
    )
