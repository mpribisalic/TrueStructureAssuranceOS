"""Tests for document upload and text extraction — Faza 3 acceptance criterion."""
import io


def test_upload_txt_document(client, auth_headers, demo_project):
    content = b"REQ-001: The system shall do something.\nREQ-002: The system shall do another thing."
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("requirements.txt", io.BytesIO(content), "text/plain")},
        data={"source_type": "requirements"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "requirements.txt"
    assert data["file_type"] == "txt"
    assert data["processing_status"] == "done"
    assert "REQ-001" in data["extracted_text"]
    assert data["file_hash"] is not None
    assert data["file_size_bytes"] == len(content)


def test_upload_md_document(client, auth_headers, demo_project):
    content = b"# Requirements\n\n## REQ-001\nThe system shall maintain safe operation."
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("requirements.md", io.BytesIO(content), "text/markdown")},
        data={"source_type": "requirements"},
    )
    assert response.status_code == 201
    assert response.json()["processing_status"] == "done"
    assert "REQ-001" in response.json()["extracted_text"]


def test_upload_json_document(client, auth_headers, demo_project):
    content = b'[{"external_test_id": "T-001", "status": "passed"}]'
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("evidence.json", io.BytesIO(content), "application/json")},
        data={"source_type": "evidence"},
    )
    assert response.status_code == 201
    assert response.json()["processing_status"] == "done"


def test_upload_csv_document(client, auth_headers, demo_project):
    content = b"external_id,title,description,test_type,automation_level,status\nT-001,Baseline test,Nominal,system,automated,active"
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("test_cases.csv", io.BytesIO(content), "text/csv")},
        data={"source_type": "test_cases"},
    )
    assert response.status_code == 201
    assert response.json()["processing_status"] == "done"


def test_upload_rejected_extension(client, auth_headers, demo_project):
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("script.exe", io.BytesIO(b"bad"), "application/octet-stream")},
        data={"source_type": "other"},
    )
    assert response.status_code == 400


def test_upload_too_large(client, auth_headers, demo_project):
    # 26 MB — exceeds 25 MB limit
    big_data = b"x" * (26 * 1024 * 1024)
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("big.txt", io.BytesIO(big_data), "text/plain")},
        data={"source_type": "other"},
    )
    assert response.status_code == 400


def test_list_documents(client, auth_headers, demo_project):
    # Upload a document first
    client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("req.txt", io.BytesIO(b"REQ-001: test"), "text/plain")},
        data={"source_type": "requirements"},
    )
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_document(client, auth_headers, demo_project):
    upload = client.post(
        f"/api/v1/projects/{demo_project.id}/documents",
        headers=auth_headers,
        files={"file": ("req.md", io.BytesIO(b"# Test\nREQ-001: test req"), "text/markdown")},
        data={"source_type": "requirements"},
    )
    doc_id = upload.json()["id"]
    response = client.get(f"/api/v1/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == doc_id


def test_document_requires_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/documents")
    assert response.status_code == 401
