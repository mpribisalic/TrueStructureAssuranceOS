"""Markdown report generator — produces all 14 sections specified in section 32."""
from datetime import datetime, timezone

_DISCLAIMER = (
    "This report is AI-assisted and does not represent formal regulatory certification "
    "or approval. All findings must be reviewed by qualified engineering, safety, "
    "compliance or mission assurance personnel."
)


def generate_markdown(
    project,
    requirements,
    test_cases,
    evidence_list,
    trace_links,
    gaps,
    readiness_score,
    ai_summary: str,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []

    def h1(t): lines.append(f"# {t}\n")
    def h2(t): lines.append(f"## {t}\n")
    def h3(t): lines.append(f"### {t}\n")
    def para(t): lines.append(f"{t}\n")
    def sep(): lines.append("---\n")
    def blank(): lines.append("")

    # ── 1. Project Summary ────────────────────────────────────────────────────
    h1(f"Certification Readiness Report: {project.name}")
    para(f"**Generated:** {now}")
    para(f"**Industry:** {project.industry.value if hasattr(project.industry, 'value') else project.industry}")
    para(f"**Criticality:** {project.criticality_level.value if hasattr(project.criticality_level, 'value') else project.criticality_level}")
    para(f"**Status:** {project.status.value if hasattr(project.status, 'value') else project.status}")
    sep()

    # ── 2. Dataset Summary ────────────────────────────────────────────────────
    h2("Dataset Summary")
    para(f"| Item | Count |")
    para(f"|------|-------|")
    para(f"| Requirements | {len(requirements)} |")
    para(f"| Test Cases | {len(test_cases)} |")
    para(f"| Evidence Records | {len(evidence_list)} |")
    para(f"| Trace Links | {len(trace_links)} |")
    para(f"| Open Gaps | {sum(1 for g in gaps if g.status.value == 'open')} |")
    blank()

    # ── 3. Extracted Requirements ─────────────────────────────────────────────
    h2("Extracted Requirements")
    if requirements:
        para("| ID | Title | Category | Criticality | Review Status |")
        para("|----|-------|----------|-------------|---------------|")
        for req in requirements:
            crit = req.criticality.value if hasattr(req.criticality, "value") else req.criticality
            review = req.human_review_status.value if hasattr(req.human_review_status, "value") else req.human_review_status
            para(f"| {req.external_id} | {_esc(req.title)} | {req.category} | {crit} | {review} |")
    else:
        para("_No requirements extracted._")
    blank()

    # ── 4. Test Cases ─────────────────────────────────────────────────────────
    h2("Test Cases")
    if test_cases:
        para("| ID | Title | Type | Automation | Status |")
        para("|----|-------|------|------------|--------|")
        for tc in test_cases:
            status = tc.status.value if hasattr(tc.status, "value") else tc.status
            para(f"| {tc.external_id} | {_esc(tc.title)} | {tc.test_type} | {tc.automation_level} | {status} |")
    else:
        para("_No test cases imported._")
    blank()

    # ── 5. Evidence Summary ───────────────────────────────────────────────────
    h2("Evidence Summary")
    if evidence_list:
        para("| Title | Type | Date |")
        para("|-------|------|------|")
        for ev in evidence_list:
            date_str = ev.evidence_date.strftime("%Y-%m-%d") if ev.evidence_date else "—"
            para(f"| {_esc(ev.title)} | {ev.evidence_type} | {date_str} |")
    else:
        para("_No evidence records found._")
    blank()

    # ── 6. Traceability Matrix ────────────────────────────────────────────────
    h2("Traceability Matrix")
    approved_links = [l for l in trace_links if l.human_review_status.value == "approved"]
    if approved_links:
        para("| Requirement ID | Target ID | Link Type | Confidence | Created By |")
        para("|---------------|-----------|-----------|------------|------------|")
        for link in approved_links:
            conf = f"{link.confidence:.2f}" if link.confidence else "—"
            para(f"| {link.source_id} | {link.target_id} | {link.link_type} | {conf} | {link.created_by} |")
    else:
        para("_No approved trace links._")
    blank()

    # ── 7. Detected Gaps ──────────────────────────────────────────────────────
    h2("Detected Gaps")
    open_gaps = [g for g in gaps if g.status.value == "open"]
    if open_gaps:
        para("| Title | Type | Severity | Recommendation |")
        para("|-------|------|----------|----------------|")
        for gap in open_gaps:
            sev = gap.severity.value if hasattr(gap.severity, "value") else gap.severity
            rec = _esc(gap.recommendation or "—")
            para(f"| {_esc(gap.title)} | {gap.gap_type.value} | {sev} | {rec} |")
    else:
        para("_No open gaps detected._")
    blank()

    # ── 8. Readiness Score ────────────────────────────────────────────────────
    h2("Readiness Score")
    if readiness_score:
        para(f"**Overall Score: {readiness_score.overall_score}/100**")
        blank()
        para("| Component | Score |")
        para("|-----------|-------|")
        para(f"| Requirement Coverage | {readiness_score.coverage_score} |")
        para(f"| Test Pass Rate | {readiness_score.test_pass_score} |")
        para(f"| Evidence Completeness | {readiness_score.evidence_score} |")
        para(f"| Risk | {readiness_score.risk_score} |")
        para(f"| Freshness | {readiness_score.freshness_score} |")
        para(f"| Human Review | {readiness_score.human_review_score} |")
    else:
        para("_No readiness score calculated yet._")
    blank()

    # ── 9. Score Explanation ──────────────────────────────────────────────────
    h2("Score Explanation")
    if readiness_score:
        para(readiness_score.explanation)
        if readiness_score.caps_applied_json:
            blank()
            h3("Score Caps Applied")
            for cap in readiness_score.caps_applied_json:
                para(f"- {cap}")
    else:
        para("_Calculate readiness score to see explanation._")
    blank()

    # ── 10. Top Blockers ──────────────────────────────────────────────────────
    h2("Top Blockers")
    blockers = readiness_score.top_blockers_json if readiness_score else []
    if blockers:
        for b in blockers:
            para(f"- {b}")
    else:
        para("_No critical blockers identified._")
    blank()

    # ── 11. Recommended Actions ───────────────────────────────────────────────
    h2("Recommended Actions")
    actions = readiness_score.recommended_actions_json if readiness_score else []
    if actions:
        for i, action in enumerate(actions, start=1):
            para(f"{i}. {action}")
    else:
        para("_No immediate actions required._")
    blank()

    # ── 12. AI Usage Disclaimer ───────────────────────────────────────────────
    h2("AI Usage Disclaimer")
    if ai_summary:
        para(f"_{ai_summary}_")
        blank()
    para(f"> **{_DISCLAIMER}**")
    blank()

    # ── 13. Human Review Disclaimer ───────────────────────────────────────────
    h2("Human Review Disclaimer")
    para(
        "All AI-extracted requirements, suggested trace links, and gap analyses in this "
        "report carry a `pending_review` status until explicitly approved by a qualified "
        "engineer. Approved items are marked accordingly. This workflow enforces human "
        "oversight before any AI output is used in certification submissions."
    )
    blank()

    # ── 14. Audit Trail Summary ───────────────────────────────────────────────
    h2("Audit Trail Summary")
    total_links = len(trace_links)
    ai_links = sum(1 for l in trace_links if l.created_by == "ai")
    approved_reqs = sum(1 for r in requirements if r.human_review_status.value == "approved")
    para(f"- Requirements reviewed and approved: **{approved_reqs}/{len(requirements)}**")
    para(f"- Trace links created by AI: **{ai_links}/{total_links}**")
    para(f"- Approved trace links: **{len(approved_links)}/{total_links}**")
    para(f"- Report generated: **{now}**")
    blank()

    sep()
    para(f"_True Structure Assurance OS — {now}_")

    return "\n".join(lines)


def _esc(text: str) -> str:
    """Escape pipe characters for Markdown tables."""
    return (text or "").replace("|", "\\|").replace("\n", " ")
