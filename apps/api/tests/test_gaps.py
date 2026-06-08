"""Tests for deterministic gap detection (7 rules) — Phase 8 acceptance criteria."""
import io
import json

# ─── Shared sample data ───────────────────────────────────────────────────────

CSV_SYSTEM_TC = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Baseline operation test,Validates nominal operation,system,automated,active\n"
)
CSV_SECURITY_TC = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Security rejection test,Tests unauthorized command rejection,security,automated,active\n"
)
CSV_SIMULATION_TC = (
    b"external_id,title,description,test_type,automation_level,status\n"
    b"T-001,Positioning degradation test,Simulates degraded positioning,simulation,automated,active\n"
)

REQ_SAFETY = b"REQ-001: The system shall maintain safe operation to protect against hazards."
REQ_SECURITY = b"REQ-001: The system shall encrypt all data to prevent unauthorized access."
REQ_GENERIC = b"REQ-001: The system shall maintain safe operation."

EVIDENCE_PASSED = json.dumps([{
    "external_test_id": "T-001", "status": "passed",
    "executed_at": "2026-06-08T10:00:00Z", "environment": "sim", "summary": "OK",
}]).encode()

EVIDENCE_FAILED = json.dumps([{
    "external_test_id": "T-001", "status": "failed",
    "executed_at": "2026-05-01T10:00:00Z", "environment": "sim", "summary": "FAIL",
}]).encode()

# 400 days old — stale for medium criticality (threshold 180d)
EVIDENCE_STALE = json.dumps([{
    "external_test_id": "T-001", "status": "passed",
    "executed_at": "2024-01-01T00:00:00Z", "environment": "sim", "summary": "Old",
}]).encode()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _upload_reqs(client, auth_headers, project_id, content):
    doc = client.post(
        f"/api/v1/projects/{project_id}/documents",
        headers=auth_headers,
        files={"file": ("req.txt", io.BytesIO(content), "text/plain")},
        data={"source_type": "requirements"},
    )
    doc_id = doc.json()["id"]
    r = client.post(f"/api/v1/documents/{doc_id}/extract-requirements", headers=auth_headers)
    return r.json()  # list of requirements


def _import_tcs(client, auth_headers, project_id, csv=CSV_SYSTEM_TC):
    r = client.post(
        f"/api/v1/projects/{project_id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("tc.csv", io.BytesIO(csv), "text/csv")},
    )
    return r.json()["test_cases"]


def _import_evidence(client, auth_headers, project_id, ev_json):
    client.post(
        f"/api/v1/projects/{project_id}/evidence/import",
        headers=auth_headers,
        files={"file": ("ev.json", io.BytesIO(ev_json), "application/json")},
    )


def _link_and_approve(client, auth_headers, project_id, req_id, tc_id):
    """Create an approved manual trace link between a requirement and test case."""
    r = client.post(
        f"/api/v1/projects/{project_id}/trace-links",
        headers=auth_headers,
        json={"source_id": req_id, "target_id": tc_id, "link_type": "verifies"},
    )
    assert r.status_code == 201
    return r.json()


def _detect(client, auth_headers, project_id):
    return client.post(f"/api/v1/projects/{project_id}/gaps/detect", headers=auth_headers)


# ─── Rule 1: Missing Test ─────────────────────────────────────────────────────

def test_rule1_missing_test(client, auth_headers, demo_project):
    """Requirement with no trace link → missing_test gap."""
    _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "missing_test" in types


# ─── Rule 2: Missing Evidence ─────────────────────────────────────────────────

def test_rule2_missing_evidence(client, auth_headers, demo_project):
    """Approved trace link but no test run → missing_evidence gap."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    tcs = _import_tcs(client, auth_headers, demo_project.id)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    # No evidence imported
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "missing_evidence" in types


# ─── Rule 3: Failed Test ──────────────────────────────────────────────────────

def test_rule3_failed_test(client, auth_headers, demo_project):
    """Failed test run → failed_test gap."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    tcs = _import_tcs(client, auth_headers, demo_project.id)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_FAILED)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "failed_test" in types


# ─── Rule 4: Missing Security Validation ─────────────────────────────────────

def test_rule4_missing_security_validation(client, auth_headers, demo_project):
    """Security requirement linked to system test (not security) → gap."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_SECURITY)
    tcs = _import_tcs(client, auth_headers, demo_project.id, csv=CSV_SYSTEM_TC)  # system type
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_PASSED)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "missing_security_validation" in types


def test_rule4_no_gap_when_security_test_linked(client, auth_headers, demo_project):
    """Security requirement linked to security-type test → no security gap."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_SECURITY)
    tcs = _import_tcs(client, auth_headers, demo_project.id, csv=CSV_SECURITY_TC)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_PASSED)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "missing_security_validation" not in types


# ─── Rule 5: Missing Safety Validation ───────────────────────────────────────

def test_rule5_missing_safety_validation(client, auth_headers, demo_project):
    """Safety requirement linked to security-only test → missing_safety_validation."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_SAFETY)
    tcs = _import_tcs(client, auth_headers, demo_project.id, csv=CSV_SECURITY_TC)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_PASSED)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "missing_safety_validation" in types


def test_rule5_no_gap_when_simulation_test_linked(client, auth_headers, demo_project):
    """Safety requirement linked to simulation test → no safety gap."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_SAFETY)
    tcs = _import_tcs(client, auth_headers, demo_project.id, csv=CSV_SIMULATION_TC)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_PASSED)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "missing_safety_validation" not in types


# ─── Rule 6: Stale Evidence ───────────────────────────────────────────────────

def test_rule6_stale_evidence(client, auth_headers, demo_project):
    """Evidence older than threshold → stale_evidence gap."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    tcs = _import_tcs(client, auth_headers, demo_project.id)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_STALE)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "stale_evidence" in types


# ─── Rule 7: Unapproved AI Suggestion ────────────────────────────────────────

def test_rule7_unapproved_ai_suggestion(client, auth_headers, demo_project):
    """AI suggested links exist but none approved → unapproved_ai_suggestion gap.

    We import a TC whose title/description shares 2+ words with the requirement text
    so MockAI's word-overlap heuristic produces at least one suggestion.
    """
    # REQ text: "maintain safe operation" — words: maintain, safe, operation
    # TC description: "maintain safe operation" — same words → overlap = 3 ≥ 2
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    csv_overlap = (
        b"external_id,title,description,test_type,automation_level,status\n"
        b"T-MATCH,Safe operation test,Maintain safe operation under normal conditions,system,automated,active\n"
    )
    client.post(
        f"/api/v1/projects/{demo_project.id}/test-cases/import",
        headers=auth_headers,
        files={"file": ("tc.csv", io.BytesIO(csv_overlap), "text/csv")},
    )
    r = client.post(
        f"/api/v1/projects/{demo_project.id}/trace-links/suggest",
        headers=auth_headers,
    )
    assert r.json()["suggested"] >= 1, "MockAI should suggest at least one link given overlapping words"
    # Do NOT approve the suggestions
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    types = [g["gap_type"] for g in response.json()["gaps"]]
    assert "unapproved_ai_suggestion" in types


# ─── General endpoint tests ───────────────────────────────────────────────────

def test_detect_clears_previous_gaps(client, auth_headers, demo_project):
    """Second detect call replaces previous gaps, not adds to them."""
    _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    r1 = _detect(client, auth_headers, demo_project.id)
    r2 = _detect(client, auth_headers, demo_project.id)
    assert r1.json()["detected"] == r2.json()["detected"]


def test_list_gaps(client, auth_headers, demo_project):
    _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    _detect(client, auth_headers, demo_project.id)
    response = client.get(f"/api/v1/projects/{demo_project.id}/gaps", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_gap_status(client, auth_headers, demo_project):
    _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    detect = _detect(client, auth_headers, demo_project.id)
    gap_id = detect.json()["gaps"][0]["id"]
    response = client.patch(
        f"/api/v1/gaps/{gap_id}",
        headers=auth_headers,
        json={"status": "acknowledged"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"


def test_no_gaps_when_fully_covered(client, auth_headers, demo_project):
    """Requirement with approved link, passed evidence, fresh date → no gaps."""
    reqs = _upload_reqs(client, auth_headers, demo_project.id, REQ_GENERIC)
    tcs = _import_tcs(client, auth_headers, demo_project.id)
    _link_and_approve(client, auth_headers, demo_project.id, reqs[0]["id"], tcs[0]["id"])
    _import_evidence(client, auth_headers, demo_project.id, EVIDENCE_PASSED)
    response = _detect(client, auth_headers, demo_project.id)
    assert response.status_code == 201
    assert response.json()["detected"] == 0


def test_gaps_require_auth(client, demo_project):
    response = client.get(f"/api/v1/projects/{demo_project.id}/gaps")
    assert response.status_code == 401
