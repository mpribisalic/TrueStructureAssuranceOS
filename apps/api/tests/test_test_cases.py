"""Tests for test case CSV import — Phase 5 acceptance criteria."""
import io

SAMPLE_CSV = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Baseline operation test,Validates nominal system operation,system,automated,active\n"
    b"T-002,Positioning degradation test,Simulates degraded positioning,simulation,automated,active\n"
    b"T-003,Communication loss detection test,Simulates comm loss,system,automated,active\n"
    b"T-004,Sensor disagreement simulation,Simulates inconsistent sensors,simulation,automated,active\n"
    b"T-005,Telemetry recording test,Checks telemetry during operation,system,automated,active\n"
)


def _import(client, auth_headers, project_id, csv_bytes=None):
    return client.post(
        f"/api/v1/projects/{project_id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("test_cases.csv", io.BytesIO(csv_bytes or SAMPLE_CSV), "text/csv")},
    )


def test_import_sample_csv(client, auth_headers, demo_project):
    response = _import(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 5
    assert data["skipped"] == 0
    assert data["errors"] == []
    ids = [tc["external_id"] for tc in data["test_cases"]]
    assert "T-001" in ids and "T-005" in ids


def test_import_idempotent(client, auth_headers, demo_project):
    _import(client, auth_headers, demo_project.id)
    r2 = _import(client, auth_headers, demo_project.id)
    assert r2.status_code == 201
    assert r2.json()["imported"] == 0
    assert r2.json()["skipped"] == 5


def test_list_test_cases(client, auth_headers, demo_project):
    _import(client, auth_headers, demo_project.id)
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/test-cases",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) >= 5


def test_get_test_case(client, auth_headers, demo_project):
    result = _import(client, auth_headers, demo_project.id)
    tc_id = result.json()["test_cases"][0]["id"]
    response = client.get(f"/api/v1/test-cases/{tc_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == tc_id


def test_import_rejects_non_csv(client, auth_headers, demo_project):
    response = client.post(
        f"/api/v1/projects/{demo_project.id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("data.json", io.BytesIO(b"[]"), "application/json")},
    )
    assert response.status_code == 400


def test_import_missing_required_column(client, auth_headers, demo_project):
    bad_csv = b"title,description\nBaseline,Some desc\n"
    response = _import(client, auth_headers, demo_project.id, csv_bytes=bad_csv)
    assert response.status_code == 400


def test_import_invalid_test_type_reported(client, auth_headers, demo_project):
    bad_csv = (
        b"external_id,title,description,test_type,automation_level,status\n"
        b"T-BAD,Bad row,Desc,unknown_type,automated,active\n"
        b"T-OK,Good row,Desc,system,automated,active\n"
    )
    response = _import(client, auth_headers, demo_project.id, csv_bytes=bad_csv)
    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 1
    assert len(data["errors"]) == 1
    assert data["errors"][0]["external_id"] == "T-BAD"


def test_import_missing_required_fields_in_row(client, auth_headers, demo_project):
    bad_csv = (
        b"external_id,title,description,test_type,automation_level,status\n"
        b",No ID row,Desc,system,automated,active\n"
        b"T-VALID,Valid row,Desc,system,automated,active\n"
    )
    response = _import(client, auth_headers, demo_project.id, csv_bytes=bad_csv)
    assert response.status_code == 201
    data = response.json()
    assert data["imported"] == 1
    assert len(data["errors"]) == 1


def test_test_cases_require_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/test-cases")
    assert response.status_code == 401
