"""Tests for evidence JSON import — Phase 6 acceptance criteria."""
import io
import json

SAMPLE_CSV = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Baseline operation test,Validates nominal operation,system,automated,active\n"
    b"T-002,Positioning degradation test,Simulates degraded positioning,simulation,automated,active\n"
    b"T-003,Communication loss detection test,Simulates comm loss,system,automated,active\n"
)

SAMPLE_EVIDENCE = [
    {
        "external_test_id": "T-001",
        "status": "passed",
        "executed_at": "2026-05-01T10:00:00Z",
        "environment": "simulation",
        "summary": "Nominal operation completed successfully.",
    },
    {
        "external_test_id": "T-002",
        "status": "passed",
        "executed_at": "2026-05-01T11:00:00Z",
        "environment": "simulation",
        "summary": "System maintained safe operation for 35 seconds.",
    },
    {
        "external_test_id": "T-003",
        "status": "passed",
        "executed_at": "2026-05-02T09:00:00Z",
        "environment": "simulation",
        "summary": "Communication loss detected in 3.8 seconds.",
    },
]


def _import_test_cases(client, auth_headers, project_id):
    client.post(
        f"/api/v1/projects/{project_id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("test_cases.csv", io.BytesIO(SAMPLE_CSV), "text/csv")},
    )


def _import_evidence(client, auth_headers, project_id, records=None):
    data = json.dumps(records or SAMPLE_EVIDENCE).encode()
    return client.post(
        f"/api/v1/projects/{project_id}/evidence/import",
        headers=auth_headers,
        files={"file": ("evidence.json", io.BytesIO(data), "application/json")},
    )


def test_import_sample_evidence(client, auth_headers, demo_project):
    _import_test_cases(client, auth_headers, demo_project.id)
    response = _import_evidence(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 3
    assert data["skipped"] == 0
    assert data["errors"] == []
    # Each evidence record is linked to a test run
    for ev in data["evidence"]:
        assert ev["test_run_id"] is not None
        assert ev["evidence_type"] == "test_result"


def test_import_creates_test_runs(client, auth_headers, demo_project):
    _import_test_cases(client, auth_headers, demo_project.id)
    _import_evidence(client, auth_headers, demo_project.id)
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/evidence",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_evidence(client, auth_headers, demo_project):
    _import_test_cases(client, auth_headers, demo_project.id)
    result = _import_evidence(client, auth_headers, demo_project.id)
    ev_id = result.json()["evidence"][0]["id"]
    response = client.get(f"/api/v1/evidence/{ev_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == ev_id


def test_import_unknown_test_case_reported(client, auth_headers, demo_project):
    _import_test_cases(client, auth_headers, demo_project.id)
    bad = [{"external_test_id": "T-UNKNOWN", "status": "passed", "executed_at": "2026-01-01T00:00:00Z"}]
    response = _import_evidence(client, auth_headers, demo_project.id, records=bad)
    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 0
    assert len(data["errors"]) == 1
    assert "not found" in data["errors"][0]["error"]


def test_import_invalid_status_reported(client, auth_headers, demo_project):
    _import_test_cases(client, auth_headers, demo_project.id)
    bad = [{"external_test_id": "T-001", "status": "unknown_status", "executed_at": "2026-01-01T00:00:00Z"}]
    response = _import_evidence(client, auth_headers, demo_project.id, records=bad)
    assert response.status_code == 201
    assert len(response.json()["errors"]) == 1


def test_import_missing_external_test_id(client, auth_headers, demo_project):
    bad = [{"status": "passed", "executed_at": "2026-01-01T00:00:00Z"}]
    response = _import_evidence(client, auth_headers, demo_project.id, records=bad)
    assert response.status_code == 201
    assert len(response.json()["errors"]) == 1


def test_import_rejects_non_json(client, auth_headers, demo_project):
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import",
        headers=auth_headers,
        files={"file": ("evidence.csv", io.BytesIO(b"a,b,c"), "text/csv")},
    )
    assert response.status_code == 400


def test_import_rejects_invalid_json(client, auth_headers, demo_project):
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import",
        headers=auth_headers,
        files={"file": ("evidence.json", io.BytesIO(b"{not json}"), "application/json")},
    )
    assert response.status_code == 400


def test_import_rejects_non_array(client, auth_headers, demo_project):
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import",
        headers=auth_headers,
        files={"file": ("evidence.json", io.BytesIO(b'{"key": "val"}'), "application/json")},
    )
    assert response.status_code == 400


def test_evidence_requires_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/evidence")
    assert response.status_code == 401
