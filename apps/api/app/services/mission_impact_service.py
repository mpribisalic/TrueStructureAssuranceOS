"""Mission Impact Engine — Phase 14.

Deterministically maps open gaps to mission impacts.
"""
import uuid

from sqlalchemy.orm import Session

from app.models.gap import Gap, GapSeverity, GapStatus, GapType
from app.models.mission_impact import ImpactCategory, ImpactLevel, MissionImpact
from app.repositories import mission_impact_repo
from app.repositories.gap_repo import get_all as get_all_gaps
from app.schemas.mission_impact import MissionImpactAnalyzeResponse, MissionImpactRead

GAP_TO_IMPACT: dict[GapType, dict] = {
    GapType.missing_security_validation: {
        "impact_category": ImpactCategory.cyber,
        "impact_level": ImpactLevel.critical,
        "title": "Security Validation Gap — Unauthorized Command Risk",
        "operational_consequence": "System may accept unauthorized commands in adversarial environments",
        "mission_consequence": "Risk of mission compromise through cyber exploitation",
        "readiness_delta": -15.0,
    },
    GapType.failed_test: {
        "impact_category": ImpactCategory.reliability,
        "impact_level": ImpactLevel.high,
        "title": "Validation Failure — Performance Below Specification",
        "operational_consequence": "System performance does not meet operational threshold",
        "mission_consequence": "Reduced mission effectiveness and increased operator workload",
        "readiness_delta": -21.0,
    },
    GapType.missing_test: {
        "impact_category": ImpactCategory.mission,
        "impact_level": ImpactLevel.high,
        "title": "Missing Test Coverage — Unvalidated Requirement",
        "operational_consequence": "Requirement has not been validated through testing",
        "mission_consequence": "Unknown mission risk from unvalidated system behavior",
        "readiness_delta": -8.0,
    },
    GapType.missing_evidence: {
        "impact_category": ImpactCategory.compliance,
        "impact_level": ImpactLevel.medium,
        "title": "Missing Evidence — Validation Chain Incomplete",
        "operational_consequence": "No evidence exists that requirement was tested",
        "mission_consequence": "Compliance with certification standards cannot be demonstrated",
        "readiness_delta": -5.0,
    },
    GapType.stale_evidence: {
        "impact_category": ImpactCategory.availability,
        "impact_level": ImpactLevel.medium,
        "title": "Stale Evidence — Validation Currency Expired",
        "operational_consequence": "Evidence may not reflect current system state",
        "mission_consequence": "Readiness assessment based on outdated validation data",
        "readiness_delta": -4.0,
    },
    GapType.missing_safety_validation: {
        "impact_category": ImpactCategory.safety,
        "impact_level": ImpactLevel.critical,
        "title": "Safety Validation Gap — Safety Case Incomplete",
        "operational_consequence": "Safety-critical requirement lacks validation evidence",
        "mission_consequence": "Mission deployment may create unacceptable safety risk",
        "readiness_delta": -18.0,
    },
    GapType.unapproved_ai_suggestion: {
        "impact_category": ImpactCategory.compliance,
        "impact_level": ImpactLevel.low,
        "title": "Unapproved AI Traceability — Human Review Pending",
        "operational_consequence": "AI-generated traceability links have not been reviewed by engineers",
        "mission_consequence": "Certification assurance confidence is reduced",
        "readiness_delta": -3.0,
    },
}

_LEVEL_ORDER = [ImpactLevel.low, ImpactLevel.medium, ImpactLevel.high, ImpactLevel.critical]


def _escalate(level: ImpactLevel, gap_severity: GapSeverity) -> ImpactLevel:
    """Escalate impact level to critical if gap severity is critical and level < critical."""
    if gap_severity == GapSeverity.critical and level != ImpactLevel.critical:
        return ImpactLevel.critical
    return level


def _build_title(base_title: str, gap: Gap) -> str:
    """Prefix with requirement external_id if available."""
    if gap.related_requirement_id is not None:
        from app.models.requirement import Requirement  # local import to avoid circular
        # We can't easily query here without the session — use gap title hint instead
        # The gap title itself often contains the external_id (e.g. "No approved test for REQ-003")
        # Extract it from gap.title if pattern found
        import re
        match = re.search(r"(REQ-\d+)", gap.title)
        if match:
            return f"{match.group(1)}: {base_title}"
    return base_title


def analyze_mission_impact(db: Session, project_id: uuid.UUID) -> MissionImpactAnalyzeResponse:
    # Clear previous impacts for this project
    mission_impact_repo.delete_by_project(db, project_id)

    # Load all open gaps
    all_gaps = get_all_gaps(db, project_id)
    open_gaps = [g for g in all_gaps if g.status == GapStatus.open]

    created: list[MissionImpact] = []
    for gap in open_gaps:
        mapping = GAP_TO_IMPACT.get(gap.gap_type)
        if mapping is None:
            continue

        impact_level = _escalate(mapping["impact_level"], gap.severity)
        title = _build_title(mapping["title"], gap)

        impact = MissionImpact(
            project_id=project_id,
            related_gap_id=gap.id,
            impact_category=mapping["impact_category"],
            impact_level=impact_level,
            title=title,
            operational_consequence=mapping["operational_consequence"],
            mission_consequence=mapping["mission_consequence"],
            readiness_delta=mapping["readiness_delta"],
        )
        mission_impact_repo.create(db, impact)
        created.append(impact)

    return MissionImpactAnalyzeResponse(analyzed=len(created), impacts=created)


def list_mission_impacts(db: Session, project_id: uuid.UUID) -> list[MissionImpact]:
    return mission_impact_repo.get_by_project(db, project_id)
