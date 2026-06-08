"""Tests for Phase 15 — Confidence Engine."""
import pytest


def test_calculate_confidence_empty_project(client, auth_headers, demo_project):
    """Empty project (no links/reqs) should return very_high confidence (nothing unapproved)."""
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/confidence/calculate",
        headers=auth_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["confidence_level"] in ("high", "very_high")
    assert 0 <= data["confidence_value"] <= 100
    assert data["explanation"]


def test_calculate_confidence_idempotent(client, auth_headers, demo_project):
    """Calling calculate twice should not create duplicate rows."""
    client.post(
        f"/api/v1/projects/{demo_project.id}/confidence/calculate",
        headers=auth_headers,
    )
    r2 = client.post(
        f"/api/v1/projects/{demo_project.id}/confidence/calculate",
        headers=auth_headers,
    )
    assert r2.status_code == 201
    # GET should return one result (not 404)
    r3 = client.get(
        f"/api/v1/projects/{demo_project.id}/confidence",
        headers=auth_headers,
    )
    assert r3.status_code == 200


def test_get_confidence_404_before_calculation(client, auth_headers, demo_project):
    r = client.get(
        f"/api/v1/projects/{demo_project.id}/confidence",
        headers=auth_headers,
    )
    assert r.status_code == 404
