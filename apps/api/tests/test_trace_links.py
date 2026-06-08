"""Tests for traceability link suggestions and approve/reject — Phase 7."""
import io

SAMPLE_CSV = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Baseline operation test,Validates nominal operation,system,automated,active\n"
    b"T-002,Positioning degradation test,Simulates degraded positioning,simulation,automated,active\n"
    b"T-003,Communication loss detection test,Simulates comm loss,system,automated,active\n"
)

REQ_CONTENT = (
    b"REQ-001: The system shall maintain safe operation under positioning degradation.\n"
    b"REQ-002: The system shall detect communication loss within 5 seconds.\n"
    b"REQ-003: The system shall record telemetry during all operation modes.\n"
)


def _setup(client, auth_headers, project_id):
    """Upload requirements doc + extract, import test cases."""
    doc = client.post(
        f"/api/v1/projects/{project_id}/documents",
        headers=auth_headers,
        files={"file": ("requirements.txt", io.BytesIO(REQ_CONTENT), "text/plain")},
        data={"source_type": "requirements"},
    )
    doc_id = doc.json()["id"]
    client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers)
    client.post(
        f"/api/v1/projects/{project_id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("test_cases.csv", io.BytesIO(SAMPLE_CSV), "text/csv")},
    )


def test_suggest_links(client, auth_headers, demo_project):
    _setup(client, auth_headers, demo_project.id)
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/trace-links/suggest",
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["suggested"] >= 1
    # All AI suggestions start as pending
    assert all(link["human_review_status"] == "pending" for link in data["links"])
    assert all(link["created_by"] == "ai" for link in data["links"])
    assert all(link["confidence"] is not None for link in data["links"])


def test_suggest_idempotent(client, auth_headers, demo_project):
    _setup(client, auth_headers, demo_project.id)
    r1 = client.post(f"/api/v1/projects/{demo_project.id}/trace-links/suggest", headers=auth_headers)
    r2 = client.post(f"/api/v1/projects/{demo_project.id}/trace-links/suggest", headers=auth_headers)
    assert r1.status_code == 201
    assert r2.status_code == 201
    # Second call: same links already exist, all skipped
    assert r2.json()["suggested"] == 0
    assert r2.json()["skipped"] == r1.json()["suggested"]


def test_list_trace_links(client, auth_headers, demo_project):
    _setup(client, auth_headers, demo_project.id)
    client.post(f"/api/v1/projects/{demo_project.id}/trace-links/suggest", headers=auth_headers)
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/trace-links",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_approve_link(client, auth_headers, demo_project):
    _setup(client, auth_headers, demo_project.id)
    suggest = client.post(
        f"/api/v1/projects/{demo_project.id}/trace-links/suggest",
        headers=auth_headers,
    )
    link_id = suggest.json()["links"][0]["id"]
    response = client.post(f"/api/v1/trace-links/{link_id}/approve", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["human_review_status"] == "approved"


def test_reject_link(client, auth_headers, demo_project):
    _setup(client, auth_headers, demo_project.id)
    suggest = client.post(
        f"/api/v1/projects/{demo_project.id}/trace-links/suggest",
        headers=auth_headers,
    )
    link_id = suggest.json()["links"][0]["id"]
    response = client.post(f"/api/v1/trace-links/{link_id}/reject", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["human_review_status"] == "rejected"


def test_suggest_no_requirements_returns_empty(client, auth_headers, demo_project):
    # No requirements or test cases — nothing to suggest
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/trace-links/suggest",
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["suggested"] == 0


def test_trace_links_require_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/trace-links")
    assert response.status_code == 401
