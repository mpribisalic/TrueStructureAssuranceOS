"""Tests for Phase 19 STANAG standards mapping stubs."""


def test_list_standards_returns_empty(client, auth_headers):
    r = client.get("/api/v1/standards", headers=auth_headers)
    assert r.status_code == 200
    assert r.json() == []


def test_standards_coverage_stub(client, auth_headers, demo_project):
    r = client.get(
        f"/api/v1/projects/{demo_project.id}/standards/coverage",
        headers=auth_headers,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["coverage_percent"] == 0.0
    assert data["standard_name"] == "STANAG (stub)"
    assert data["total_clauses"] == 0
    assert data["covered_clauses"] == 0
    assert data["missing_clauses"] == []
    assert data["standard_id"] is None
