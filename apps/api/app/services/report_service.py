"""Report generation service — assembles project data and renders Markdown."""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.core.errors import NotFoundError
from app.models.report import Report
from app.repositories import report_repo
from app.repositories.evidence_repo import get_evidence_all
from app.repositories.gap_repo import get_all as get_all_gaps
from app.repositories.readiness_repo import get_latest as get_latest_readiness
from app.repositories.requirement_repo import get_all as get_all_requirements
from app.repositories.test_case_repo import get_all as get_all_test_cases
from app.repositories.trace_link_repo import get_all as get_all_links
from app.reports.generator import generate_markdown
from app.schemas.report import ReportCreate


def create_report(
    db: Session,
    project_id: uuid.UUID,
    payload: ReportCreate,
    created_by_user_id: uuid.UUID,
) -> Report:
    # Fetch project
    from app.models.project import Project
    project = db.get(Project, project_id)
    if not project:
        raise NotFoundError("Project not found")

    # Gather all required data
    requirements = get_all_requirements(db, project_id)
    test_cases = get_all_test_cases(db, project_id)
    evidence_list = get_evidence_all(db, project_id)
    trace_links = get_all_links(db, project_id)
    gaps = get_all_gaps(db, project_id)
    readiness_score = get_latest_readiness(db, project_id)

    # AI-generated summary (safe to call; mock provider works offline)
    ai = get_ai_provider()
    ai_result = ai.generate_report_summary(context={
        "project": project.name,
        "requirements": len(requirements),
        "test_cases": len(test_cases),
        "gaps": len(gaps),
    })

    content = generate_markdown(
        project=project,
        requirements=requirements,
        test_cases=test_cases,
        evidence_list=evidence_list,
        trace_links=trace_links,
        gaps=gaps,
        readiness_score=readiness_score,
        ai_summary=ai_result.summary,
    )

    title = payload.title or f"{project.name} — Readiness Report {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"

    report = Report(
        project_id=project_id,
        readiness_score_id=readiness_score.id if readiness_score else None,
        title=title,
        report_type=payload.report_type,
        format="markdown",
        content_markdown=content,
        created_by_user_id=created_by_user_id,
    )
    report_repo.create(db, report)
    db.flush()
    return report


def list_reports(db: Session, project_id: uuid.UUID) -> list[Report]:
    return report_repo.get_all(db, project_id)


def get_report(db: Session, report_id: uuid.UUID) -> Report:
    report = report_repo.get_by_id(db, report_id)
    if not report:
        raise NotFoundError("Report not found")
    return report
