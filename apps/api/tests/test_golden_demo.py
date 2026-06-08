"""Golden demo test — loads the full defense-autonomy sample dataset and verifies
TRL 4 acceptance criteria:

    requirements >= 8
    test_cases >= 5
    gaps >= 3
    readiness_score in [50, 85]
    critical_or_high_gaps >= 2
    report generated successfully

This test doubles as living documentation of the prototype's end-to-end behavior.
"""
import io
import json
from pathlib import Path

import pytest

SAMPLES = Path(__file__).parent.parent.parent.parent / "samples" / "defense-autonomy"


@pytest.fixture
def sample_requirements():
    return (SAMPLES / "requirements.md").read_bytes()


@pytest.fixture
def sample_test_cases():
    return (SAMPLES / "test_cases.csv").read_bytes()


@pytest.fixture
def sample_evidence():
    return (SAMPLES / "evidence.json").read_bytes()


def test_golden_demo_full_flow(
    client,
    auth_headers,
    demo_project,
    sample_requirements,
    sample_test_cases,
    sample_evidence,
):
    """End-to-end: upload → extract → import → link → detect → score → report."""
    pid = demo_project.id

    # 1. Upload and extract requirements
    doc_r = client.post(
        f"/api/v1/projects/{pid}/documents",
        headers=auth_headers,
        files={"file": ("requirements.md", io.BytesIO(sample_requirements), "text/markdown")},
        data={"source_type": "requirements"},
    )
    assert doc_r.status_code == 201
    doc_id = doc_r.json()["id"]

    extract_r = client.post(
        f"/api/v1/documents/{doc_id}/extract-requirements",
        headers=auth_headers,
    )
    assert extract_r.status_code == 201
    requirements = extract_r.json()
    assert len(requirements) >= 8, f"Expected ≥8 requirements, got {len(requirements)}"

    # 2. Import test cases
    tc_r = client.post(
        f"/api/v1/projects/{pid}/test-cases/import",
        headers=auth_headers,
        files={"file": ("test_cases.csv", io.BytesIO(sample_test_cases), "text/csv")},
    )
    assert tc_r.status_code == 201
    test_cases = tc_r.json()["test_cases"]
    assert len(test_cases) >= 5, f"Expected ≥5 test cases, got {len(test_cases)}"

    # 3. Import evidence
    ev_r = client.post(
        f"/api/v1/projects/{pid}/evidence/import",
        headers=auth_headers,
        files={"file": ("evidence.json", io.BytesIO(sample_evidence), "application/json")},
    )
    assert ev_r.status_code == 201
    ev_data = ev_r.json()
    assert ev_data["imported"] >= 5

    # 4. AI-suggest trace links and approve matching ones
    suggest_r = client.post(
        f"/api/v1/projects/{pid}/trace-links/suggest",
        headers=auth_headers,
    )
    assert suggest_r.status_code == 201
    for link in suggest_r.json()["links"]:
        client.post(f"/api/v1/trace-links/{link['id']}/approve", headers=auth_headers)

    # Manually link requirements that AI may have missed
    req_by_id_str = {r["external_id"]: r["id"] for r in requirements}
    tc_by_id_str = {t["external_id"]: t["id"] for t in test_cases}

    manual_links = [
        ("REQ-001", "T-002"),
        ("REQ-002", "T-003"),
        ("REQ-003", "T-004"),
        ("REQ-004", "T-005"),
        ("REQ-005", "T-001"),
    ]
    for req_ext, tc_ext in manual_links:
        req_id = req_by_id_str.get(req_ext)
        tc_id = tc_by_id_str.get(tc_ext)
        if req_id and tc_id:
            client.post(
                f"/api/v1/projects/{pid}/trace-links",
                headers=auth_headers,
                json={"source_id": req_id, "target_id": tc_id, "link_type": "verifies"},
            )

    # 5. Detect gaps
    gap_r = client.post(f"/api/v1/projects/{pid}/gaps/detect", headers=auth_headers)
    assert gap_r.status_code == 201
    gaps = gap_r.json()["gaps"]
    assert gap_r.json()["detected"] >= 3, (
        f"Expected ≥3 gaps, got {gap_r.json()['detected']}"
    )

    critical_or_high = sum(
        1 for g in gaps if g["severity"] in ("critical", "high") and g["status"] == "open"
    )
    assert critical_or_high >= 2, (
        f"Expected ≥2 critical/high gaps, got {critical_or_high}"
    )

    # 6. Calculate readiness
    score_r = client.post(
        f"/api/v1/projects/{pid}/readiness/calculate",
        headers=auth_headers,
    )
    assert score_r.status_code == 201
    score = score_r.json()["overall_score"]
    assert 50 <= score <= 85, (
        f"Expected readiness score 50–85, got {score}. "
        f"Caps: {score_r.json()['caps_applied_json']}"
    )

    # 7. Generate report
    report_r = client.post(
        f"/api/v1/projects/{pid}/reports",
        headers=auth_headers,
        json={"title": "DIANA TRL 4 Readiness Report — Autonomous Reconnaissance Sensor Platform"},
    )
    assert report_r.status_code == 201
    md = report_r.json()["content_markdown"]
    assert "# Certification Readiness Report" in md
    assert "REQ-001" in md
    assert "T-001" in md
    assert "does not represent formal regulatory certification" in md

    # 8. Verify download
    report_id = report_r.json()["id"]
    dl = client.get(f"/api/v1/reports/{report_id}/download", headers=auth_headers)
    assert dl.status_code == 200
    assert "text/markdown" in dl.headers["content-type"]
