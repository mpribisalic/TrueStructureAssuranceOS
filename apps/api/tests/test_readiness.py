"""Tests for readiness scoring engine — Phase 9 acceptance criteria."""
import io
import json

# ─── Shared helpers (mirrors test_gaps.py setup) ─────────────────────────────

CSV_SYSTEM_TC = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Baseline operation test,Validates nominal operation,system,automated,active\n"
)

EVIDENCE_PASSED_FRESH = json.dumps([{
    "external_test_id": "T-001", "status": "passed",
    "executed_at": "2026-06-08T10:00:00Z", "environment": "sim", "summary": "OK",
}]).encode()

EVIDENCE_FAILED = json.dumps([{
    "external_test_id": "T-001", "status": "failed",
    "executed_at": "2026-06-08T10:00:00Z", "environment": "sim", "summary": "FAIL",
}]).encode()

EVIDENCE_STALE = json.dumps([{
    "external_test_id": "T-001", "status": "passed",
    "executed_at": "2024-01-01T00:00:00Z", "environment": "sim", "summary": "Old",
}]).encode()


def _upload_extract(client, auth_headers, project_id, content):
    doc = client.post(
        f"/api/v1/projects/{project_id}/documents",
        headers=auth_headers,
        files={"file": ("req.txt", io.BytesIO(content), "text/plain")},
        data={"source_type": "requirements"},
    )
    doc_id = doc.json()["id"]
    r = client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers)
    return r.json()


def _import_tc(client, auth_headers, project_id, csv=CSV_SYSTEM_TC):
    r = client.post(
        f"/api/v1/projects/{project_id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("tc.csv", io.BytesIO(csv), "text/csv")},
    )
    return r.json()["test_cases"]


def _import_ev(client, auth_headers, project_id, ev):
    client.post(
        f"/api/v1/projects/{project_id}/evidence/import",
        headers=auth_headers,
        files={"file": ("ev.json", io.BytesIO(ev), "application/json")},
    )


def _link(client, auth_headers, project_id, req_id, tc_id):
    client.post(
        f"/api/v1/projects/{project_id}/trace-links",
        headers=auth_headers,
        json={"source_id": req_id, "target_id": tc_id, "link_type": "verifies"},
    )


def _calculate(client, auth_headers, project_id):
    return client.post(
        f"/api/v1/projects/{project_id}/readiness/calculate",
        headers=auth_headers,
    )


# ─── Basic scoring ────────────────────────────────────────────────────────────

def test_score_has_all_components(client, auth_headers, demo_project):
    response = _calculate(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    data = response.json()
    for field in ["overall_score", "coverage_score", "test_pass_score", "evidence_score",
                  "risk_score", "freshness_score", "human_review_score"]:
        assert field in data
    assert isinstance(data["caps_applied_json"], list)
    assert isinstance(data["top_blockers_json"], list)
    assert isinstance(data["recommended_actions_json"], list)
    assert data["explanation"]


def test_empty_project_scores_zero(client, auth_headers, demo_project):
    data = _calculate(client, auth_headers, demo_project.id).json()
    # No requirements → coverage/evidence/freshness = 0; no gaps → risk = 100;
    # no AI links → human_review = 100. Formula gives 0.10*100 + 0.05*100 = 15.
    assert data["overall_score"] == 15.0
    assert data["coverage_score"] == 0.0


def test_fully_covered_project_scores_high(client, auth_headers, demo_project):
    reqs = _upload_extract(client, auth_headers, demo_project.id,
                           b"REQ-001: The system shall perform baseline operations.")
    tcs = _import_tc(client, auth_headers, demo_project.id)
    _link(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_ev(client, auth_headers, demo_project.id, EVIDENCE_PASSED_FRESH)
    data = _calculate(client, auth_headers, demo_project.id).json()
    assert data["coverage_score"] == 100.0
    assert data["test_pass_score"] == 100.0
    assert data["evidence_score"] == 100.0
    assert data["overall_score"] > 70.0


# ─── Score caps ───────────────────────────────────────────────────────────────

def test_cap_no_evidence_max49(client, auth_headers, demo_project):
    """No evidence at all → score capped at 49."""
    reqs = _upload_extract(client, auth_headers, demo_project.id,
                           b"REQ-001: The system shall perform baseline operations.")
    tcs = _import_tc(client, auth_headers, demo_project.id)
    _link(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    # No evidence imported
    data = _calculate(client, auth_headers, demo_project.id).json()
    assert data["overall_score"] <= 49.0
    assert any("49" in c for c in data["caps_applied_json"])


def test_cap_failed_critical_test_max74(client, auth_headers, demo_project):
    """Critical requirement with a failed test run → capped at 74."""
    # "critical" keyword in text triggers critical criticality in MockAI
    reqs = _upload_extract(
        client, auth_headers, demo_project.id,
        b"REQ-001: The system shall maintain critical safe operation under all conditions.",
    )
    tcs = _import_tc(client, auth_headers, demo_project.id)
    _link(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_ev(client, auth_headers, demo_project.id, EVIDENCE_FAILED)
    data = _calculate(client, auth_headers, demo_project.id).json()
    assert data["overall_score"] <= 74.0
    assert any("74" in c for c in data["caps_applied_json"])


def test_cap_30pct_without_tests_max79(client, auth_headers, demo_project):
    """More than 30% requirements without tests → capped at 79."""
    # Upload 3 requirements, link only 1
    reqs = _upload_extract(
        client, auth_headers, demo_project.id,
        b"REQ-001: The system shall do A.\nREQ-002: The system shall do B.\nREQ-003: The system shall do C.",
    )
    tcs = _import_tc(client, auth_headers, demo_project.id)
    # Only link first requirement
    _link(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_ev(client, auth_headers, demo_project.id, EVIDENCE_PASSED_FRESH)
    data = _calculate(client, auth_headers, demo_project.id).json()
    assert data["overall_score"] <= 79.0
    assert any("79" in c for c in data["caps_applied_json"])


# ─── History and retrieval ────────────────────────────────────────────────────

def test_history_accumulates(client, auth_headers, demo_project):
    _calculate(client, auth_headers, demo_project.id)
    _calculate(client, auth_headers, demo_project.id)
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/readiness/history",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_latest(client, auth_headers, demo_project):
    _calculate(client, auth_headers, demo_project.id)
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/readiness/latest",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert "overall_score" in response.json()


def test_latest_404_when_no_calculation(client, auth_headers, demo_project):
    response = client.get(
        f"/api/v1/projects/{demo_project.id}/readiness/latest",
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_readiness_requires_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/readiness/latest")
    assert response.status_code == 401
