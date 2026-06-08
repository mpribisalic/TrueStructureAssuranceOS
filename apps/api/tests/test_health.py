"""Tests for the /health endpoint — Faza 1 acceptance criterion."""


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ok", "degraded")  # degraded if DB not connected
    assert data["app"] == "True Structure Assurance OS"
    assert "env" in data
    assert "database" in data


def test_health_database_connected(client):
    """Database must be reachable in the test environment."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"
