"""Tests for Phase 14 — Mission Impact Engine."""
import io

from app.models.gap import Gap, GapSeverity, GapStatus, GapType


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _seed_gaps(db, project_id, gap_types: list[GapType]) -> list[Gap]:
    gaps = []
    for gt in gap_types:
        g = Gap(
            project_id=project_id,
            gap_type=gt,
            title=f"Test gap {gt.value}",
            description="Auto-generated test gap",
            severity=GapSeverity.high,
            status=GapStatus.open,
        )
        db.add(g)
        gaps.append(g)
    db.flush()
    return gaps


# ─── Tests ───────────────────────────────────────────────────────────────────

def test_analyze_returns_impacts_for_project_with_gaps(client, auth_headers, demo_project, db):
    _seed_gaps(db, demo_project.id, [GapType.missing_test, GapType.failed_test])

    response = client.post(
        f"/api/v1/projects/{demo_project.id}/mission-impact/analyze",
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["analyzed"] == 2
    assert len(data["impacts"]) == 2


def test_analyze_clears_previous_impacts(client, auth_headers, demo_project, db):
    _seed_gaps(db, demo_project.id, [GapType.missing_test, GapType.failed_test])

    r1 = client.post(
        f"/api/v1/projects/{demo_project.id}/mission-impact/analyze",
        headers=auth_headers,
    )
    assert r1.status_code == 201

    r2 = client.post(
        f"/api/v1/projects/{demo_project.id}/mission-impact/analyze",
        headers=auth_headers,
    )
    assert r2.status_code == 201
    data = r2.json()
    # Count should not double — should still be 2, not 4
    assert data["analyzed"] == 2
    assert len(data["impacts"]) == 2


def test_get_mission_impact_list(client, auth_headers, demo_project, db):
    _seed_gaps(db, demo_project.id, [GapType.missing_safety_validation])

    client.post(
        f"/api/v1/projects/{demo_project.id}/mission-impact/analyze",
        headers=auth_headers,
    )

    response = client.get(
        f"/api/v1/projects/{demo_project.id}/mission-impact",
        headers=auth_headers,
    )
    assert response.status_code == 200
    impacts = response.json()
    assert len(impacts) == 1
    assert impacts[0]["impact_category"] == "safety"
    assert impacts[0]["impact_level"] == "critical"
