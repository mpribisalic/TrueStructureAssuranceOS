"""Tests for ATVP Connector — Phase 16 acceptance criteria."""

SAMPLE_ATVP = {
    "platform": "ATVP",
    "version": "1.0",
    "scenario": "GPS_DENIAL",
    "results": [
        {
            "test_id": "GPS_DENIAL_001",
            "test_name": "GPS Recovery Time Validation",
            "status": "FAILED",
            "metric": "recovery_time_seconds",
            "expected": 30,
            "actual": 48,
            "score": 61,
            "notes": "Recovery time exceeded specification",
        },
        {
            "test_id": "NET_001",
            "test_name": "Network Resilience",
            "status": "PASSED",
            "score": 95,
        },
    ],
}


def test_import_atvp_creates_evidence(client, auth_headers, demo_project):
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import-atvp",
        headers=auth_headers,
        json=SAMPLE_ATVP,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["imported"] == 2
    assert data["skipped"] == 0
    assert len(data["evidence_ids"]) == 2


def test_import_atvp_idempotent(client, auth_headers, demo_project):
    client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import-atvp",
        headers=auth_headers,
        json=SAMPLE_ATVP,
    )
    r2 = client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import-atvp",
        headers=auth_headers,
        json=SAMPLE_ATVP,
    )
    assert r2.status_code == 201
    data = r2.json()
    assert data["imported"] == 0
    assert data["skipped"] == 2


def test_import_atvp_failed_status_creates_failed_test_run(client, auth_headers, demo_project):
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/evidence/import-atvp",
        headers=auth_headers,
        json=SAMPLE_ATVP,
    )
    assert r.status_code == 201
    # Check evidence was created
    ev_r = client.get(f"/api/v1/projects/{demo_project.id}/evidence", headers=auth_headers)
    assert ev_r.status_code == 200
    evidence = ev_r.json()
    assert any("GPS" in e.get("title", "") for e in evidence)
