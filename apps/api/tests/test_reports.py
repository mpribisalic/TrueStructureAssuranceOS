"""Tests for Markdown report generation — Phase 10 acceptance criteria."""
import io
import json


CSV_TC = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Baseline operation test,Validates nominal operation,system,automated,active\n"
)
EVIDENCE = json.dumps([{
    "external_test_id": "T-001", "status": "passed",
    "executed_at": "2026-06-08T10:00:00Z", "environment": "sim", "summary": "OK",
}]).encode()


def _setup_full(client, auth_headers, project_id):
    """Upload requirements, test cases, evidence, trace links, gaps, readiness."""
    # Requirements
    doc = client.post(
        f"/api/v1/projects/{project_id}/documents",
        headers=auth_headers,
        files={"file": ("req.txt", io.BytesIO(b"REQ-001: The system shall perform baseline operations."), "text/plain")},
        data={"source_type": "requirements"},
    )
    doc_id = doc.json()["id"]
    reqs = client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers).json()
    # Test cases
    tcs = client.post(
        f"/api/v1/projects/{project_id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("tc.csv", io.BytesIO(CSV_TC), "text/csv")},
    ).json()["test_cases"]
    # Trace link
    client.post(
        f"/api/v1/projects/{project_id}/trace-links",
        headers=auth_headers,
        json={"source_id": reqs[0]["id"], "target_id": tcs[0]["id"], "link_type": "verifies"},
    )
    # Evidence
    client.post(
        f"/api/v1/projects/{project_id}/evidence/import",
        headers=auth_headers,
        files={"file": ("ev.json", io.BytesIO(EVIDENCE), "application/json")},
    )
    # Gaps + Readiness
    client.post(f"/api/v1/projects/{project_id}/gaps/detect", headers=auth_headers)
    client.post(f"/api/v1/projects/{project_id}/readiness/calculate", headers=auth_headers)


def test_generate_report(client, auth_headers, demo_project):
    _setup_full(client, auth_headers, demo_project.id)
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"title": "Test Readiness Report", "report_type": "readiness"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Readiness Report"
    assert data["format"] == "markdown"
    assert data["content_markdown"] is not None
    assert len(data["content_markdown"]) > 100


def test_report_contains_all_sections(client, auth_headers, demo_project):
    _setup_full(client, auth_headers, demo_project.id)
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    md = r.json()["content_markdown"]
    # All 14 required sections
    assert "# Certification Readiness Report" in md
    assert "## Dataset Summary" in md
    assert "## Extracted Requirements" in md
    assert "## Test Cases" in md
    assert "## Evidence Summary" in md
    assert "## Traceability Matrix" in md
    assert "## Detected Gaps" in md
    assert "## Readiness Score" in md
    assert "## Score Explanation" in md
    assert "## Top Blockers" in md
    assert "## Recommended Actions" in md
    assert "## AI Usage Disclaimer" in md
    assert "## Human Review Disclaimer" in md
    assert "## Audit Trail Summary" in md


def test_report_contains_disclaimer(client, auth_headers, demo_project):
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    md = r.json()["content_markdown"]
    assert "does not represent formal regulatory certification" in md


def test_report_contains_project_data(client, auth_headers, demo_project):
    _setup_full(client, auth_headers, demo_project.id)
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    md = r.json()["content_markdown"]
    assert "REQ-001" in md
    assert "T-001" in md


def test_list_reports(client, auth_headers, demo_project):
    client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    response = client.get(f"/api/v1/projects/{demo_project.id}/reports", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_report(client, auth_headers, demo_project):
    created = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    report_id = created.json()["id"]
    response = client.get(f"/api/v1/reports/{report_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == report_id


def test_download_report_returns_markdown(client, auth_headers, demo_project):
    created = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    report_id = created.json()["id"]
    response = client.get(f"/api/v1/reports/{report_id}/download", headers=auth_headers)
    assert response.status_code == 200
    assert "text/markdown" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    assert "# Certification Readiness Report" in response.text


def test_report_auto_title_when_none(client, auth_headers, demo_project):
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/reports",
        headers=auth_headers,
        json={"report_type": "readiness"},
    )
    assert r.status_code == 201
    assert "Readiness Report" in r.json()["title"]


def test_reports_require_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/reports")
    assert response.status_code == 401
