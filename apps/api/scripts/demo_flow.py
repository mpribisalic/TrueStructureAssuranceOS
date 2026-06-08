"""5-minute DIANA demo flow script.

Loads the full defense-autonomy sample dataset into the demo project via the
live API, reproducing the golden demo end-to-end.

Run:
    # 1. Start the API server
    uv run uvicorn app.main:app --reload

    # 2. In another terminal, run seed first if needed
    uv run python scripts/seed_demo.py

    # 3. Run this demo flow
    uv run python scripts/demo_flow.py

Expected output: readiness score in range 50–85, gaps listed, report URL printed.
"""
import json
import sys
from pathlib import Path

import httpx

BASE = "http://localhost:8000/api/v1"
SAMPLES = Path(__file__).parent.parent.parent.parent / "samples" / "defense-autonomy"

EMAIL = "demo@assuranceos.local"
PASSWORD = "demo1234"


def step(n, title):
    print(f"\n{'='*60}")
    print(f"  Step {n}: {title}")
    print(f"{'='*60}")


def ok(msg):
    print(f"  ✓ {msg}")


def fail(msg, r=None):
    print(f"  ✗ {msg}")
    if r is not None:
        print(f"    {r.status_code}: {r.text[:200]}")
    sys.exit(1)


def main():
    client = httpx.Client(timeout=30)

    # ── Step 1: Login ─────────────────────────────────────────────────────────
    step(1, "Login")
    r = client.post(f"{BASE}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    if r.status_code != 200:
        fail("Login failed — run scripts/seed_demo.py first", r)
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    ok(f"Logged in as {EMAIL}")

    # ── Step 2: Get demo project ───────────────────────────────────────────────
    step(2, "Get demo project")
    r = client.get(f"{BASE}/projects", headers=headers)
    projects = r.json()
    project = next((p for p in projects if "Reconnaissance" in p["name"]), None)
    if not project:
        fail("Demo project not found — run scripts/seed_demo.py first")
    pid = project["id"]
    ok(f"Project: {project['name']} (id={pid})")

    # ── Step 3: Upload and extract requirements ───────────────────────────────
    step(3, "Upload requirements and extract")
    req_bytes = (SAMPLES / "requirements.md").read_bytes()
    r = client.post(
        f"{BASE}/projects/{pid}/documents",
        headers=headers,
        files={"file": ("requirements.md", req_bytes, "text/markdown")},
        data={"source_type": "requirements"},
    )
    if r.status_code != 201:
        fail("Document upload failed", r)
    doc_id = r.json()["id"]
    ok(f"Uploaded requirements.md (doc_id={doc_id})")

    r = client.post(f"{BASE}/documents/{doc_id}/extract-requirements", headers=headers)
    if r.status_code != 201:
        fail("Requirement extraction failed", r)
    reqs = r.json()
    ok(f"Extracted {len(reqs)} requirements")
    for req in reqs:
        print(f"    {req['external_id']}: {req['title'][:60]}")

    # ── Step 4: Import test cases ─────────────────────────────────────────────
    step(4, "Import test cases from CSV")
    tc_bytes = (SAMPLES / "test_cases.csv").read_bytes()
    r = client.post(
        f"{BASE}/projects/{pid}/test-cases/import",
        headers=headers,
        files={"file": ("test_cases.csv", tc_bytes, "text/csv")},
    )
    if r.status_code != 201:
        fail("Test case import failed", r)
    tc_data = r.json()
    ok(f"Imported {tc_data['imported']} test cases (skipped: {tc_data['skipped']})")
    test_cases = tc_data["test_cases"]

    # ── Step 5: Import evidence ───────────────────────────────────────────────
    step(5, "Import evidence from JSON")
    ev_bytes = (SAMPLES / "evidence.json").read_bytes()
    r = client.post(
        f"{BASE}/projects/{pid}/evidence/import",
        headers=headers,
        files={"file": ("evidence.json", ev_bytes, "application/json")},
    )
    if r.status_code != 201:
        fail("Evidence import failed", r)
    ev_data = r.json()
    ok(f"Imported {ev_data['imported']} evidence records (errors: {len(ev_data['errors'])})")

    # ── Step 6: Suggest and approve trace links ───────────────────────────────
    step(6, "AI trace link suggestions → approve all")
    r = client.post(f"{BASE}/projects/{pid}/trace-links/suggest", headers=headers)
    if r.status_code != 201:
        fail("Trace link suggestion failed", r)
    suggest_data = r.json()
    ok(f"Suggested {suggest_data['suggested']} links (skipped: {suggest_data['skipped']})")
    for link in suggest_data["links"]:
        client.post(f"{BASE}/trace-links/{link['id']}/approve", headers=headers)
    ok(f"Approved {suggest_data['suggested']} AI-suggested links")

    # Manual links for known pairs
    req_map = {r["external_id"]: r["id"] for r in reqs}
    tc_map = {t["external_id"]: t["id"] for t in test_cases}
    manual = [("REQ-001","T-002"),("REQ-002","T-003"),("REQ-003","T-004"),("REQ-004","T-005"),("REQ-005","T-001")]
    added = 0
    for req_ext, tc_ext in manual:
        if req_map.get(req_ext) and tc_map.get(tc_ext):
            r2 = client.post(
                f"{BASE}/projects/{pid}/trace-links",
                headers=headers,
                json={"source_id": req_map[req_ext], "target_id": tc_map[tc_ext], "link_type": "verifies"},
            )
            if r2.status_code == 201:
                added += 1
    ok(f"Added {added} manual trace links")

    # ── Step 7: Detect gaps ───────────────────────────────────────────────────
    step(7, "Detect gaps (7 deterministic rules)")
    r = client.post(f"{BASE}/projects/{pid}/gaps/detect", headers=headers)
    if r.status_code != 201:
        fail("Gap detection failed", r)
    gap_data = r.json()
    ok(f"Detected {gap_data['detected']} gaps:")
    for gap in gap_data["gaps"]:
        sev = gap["severity"].upper()
        print(f"    [{sev}] {gap['gap_type']}: {gap['title']}")

    # ── Step 8: Calculate readiness ───────────────────────────────────────────
    step(8, "Calculate readiness score")
    r = client.post(f"{BASE}/projects/{pid}/readiness/calculate", headers=headers)
    if r.status_code != 201:
        fail("Readiness calculation failed", r)
    score_data = r.json()
    score = score_data["overall_score"]
    ok(f"Overall score: {score}/100")
    print(f"    Coverage:     {score_data['coverage_score']}")
    print(f"    Test pass:    {score_data['test_pass_score']}")
    print(f"    Evidence:     {score_data['evidence_score']}")
    print(f"    Risk:         {score_data['risk_score']}")
    print(f"    Freshness:    {score_data['freshness_score']}")
    print(f"    Human review: {score_data['human_review_score']}")
    if score_data["caps_applied_json"]:
        print(f"    Caps applied:")
        for cap in score_data["caps_applied_json"]:
            print(f"      - {cap}")

    # ── Step 9: Generate report ───────────────────────────────────────────────
    step(9, "Generate Markdown report")
    r = client.post(
        f"{BASE}/projects/{pid}/reports",
        headers=headers,
        json={"title": "DIANA TRL 4 Readiness Report — Autonomous Reconnaissance Sensor Platform"},
    )
    if r.status_code != 201:
        fail("Report generation failed", r)
    report_data = r.json()
    ok(f"Report generated: {report_data['title']}")
    ok(f"Download: GET {BASE}/reports/{report_data['id']}/download")
    ok(f"Content length: {len(report_data['content_markdown'])} characters")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  DEMO COMPLETE")
    print(f"{'='*60}")
    print(f"  Requirements:  {len(reqs)}")
    print(f"  Test cases:    {len(test_cases)}")
    print(f"  Gaps detected: {gap_data['detected']}")
    print(f"  Score:         {score}/100")
    category = (
        "Ready for TRL 4" if score >= 90
        else "Conditionally ready" if score >= 75
        else "Needs remediation" if score >= 60
        else "Not ready — critical blockers"
    )
    print(f"  Category:      {category}")
    print()


if __name__ == "__main__":
    main()
