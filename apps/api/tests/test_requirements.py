"""Tests for requirement extraction and CRUD — Phase 4 acceptance criteria."""
import io


def _upload_req_doc(client, auth_headers, project_id, content=None):
    if content is None:
        content = b"REQ-001: The system shall maintain safe operation.\nREQ-002: The system shall log all commands."
    r = client.post(
        f"/api/v1/projects/{project_id}/documents",
        headers=auth_headers,
        files={"file": ("requirements.txt", io.BytesIO(content), "text/plain")},
        data={"source_type": "requirements"},
    )
    assert r.status_code == 201
    return r.json()["id"]


def test_extract_requirements(client, auth_headers, demo_project):
    doc_id = _upload_req_doc(client, auth_headers, demo_project.id)
    response = client.post(
        f"/api/v1/documents/{doc_id}/extract-requirements",
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data) >= 2
    ids = [r["external_id"] for r in data]
    assert "REQ-001" in ids
    assert "REQ-002" in ids
    # All AI-extracted must be pending review
    assert all(r["human_review_status"] == "pending" for r in data)
    assert all(r["ai_confidence"] is not None for r in data)


def test_extract_idempotent(client, auth_headers, demo_project):
    doc_id = _upload_req_doc(client, auth_headers, demo_project.id)
    r1 = client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers)
    r2 = client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers)
    # Second call should return 0 new (already exist)
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert len(r2.json()) == 0


def test_list_requirements(client, auth_headers, demo_project):
    doc_id = _upload_req_doc(client, auth_headers, demo_project.id)
    client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers)
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_create_requirement_manually(client, auth_headers, demo_project):
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
        json={
            "external_id": "REQ-MANUAL-001",
            "title": "Manual requirement",
            "text": "The system shall do something manually specified.",
            "category": "functional",
            "criticality": "medium",
            "verification_method": "test",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["external_id"] == "REQ-MANUAL-001"
    assert data["human_review_status"] == "pending"
    assert data["ai_confidence"] is None


def test_create_duplicate_requirement_rejected(client, auth_headers, demo_project):
    payload = {
        "external_id": "REQ-DUP-001",
        "title": "Dup",
        "text": "Duplicate requirement.",
    }
    r1 = client.post(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
        json=payload,
    )
    r2 = client.post(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
        json=payload,
    )
    assert r1.status_code == 201
    assert r2.status_code == 409


def test_update_requirement(client, auth_headers, demo_project):
    create_r = client.post(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
        json={"external_id": "REQ-U-001", "title": "Old title", "text": "Old text."},
    )
    req_id = create_r.json()["id"]
    response = client.patch(
        f"/api/v1/requirements/{req_id}",
        headers=auth_headers,
        json={"title": "Updated title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


def test_approve_requirement(client, auth_headers, demo_project):
    create_r = client.post(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
        json={"external_id": "REQ-A-001", "title": "To approve", "text": "Approve me."},
    )
    req_id = create_r.json()["id"]
    response = client.post(f"/api/v1/requirements/{req_id}/approve", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["human_review_status"] == "approved"


def test_reject_requirement(client, auth_headers, demo_project):
    create_r = client.post(
        f"/api/v1/projects/{demo_project.id}/requirements",
        headers=auth_headers,
        json={"external_id": "REQ-R-001", "title": "To reject", "text": "Reject me."},
    )
    req_id = create_r.json()["id"]
    response = client.post(f"/api/v1/requirements/{req_id}/reject", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["human_review_status"] == "rejected"


def test_requirements_require_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/requirements")
    assert response.status_code == 401


def test_extract_from_markdown(client, auth_headers, demo_project):
    content = b"# Requirements\n\n## REQ-010\nThe system shall maintain safe operation for at least 30 seconds.\n\n## REQ-011\nThe system shall encrypt all data at rest.\n"
    doc_id = _upload_req_doc(client, auth_headers, demo_project.id, content=content)
    response = client.post(
        f"/api/v1/documents/{doc_id}/extract-requirements",
        headers=auth_headers,
    )
    assert response.status_code == 201
    ids = [r["external_id"] for r in response.json()]
    assert "REQ-010" in ids
    assert "REQ-011" in ids
