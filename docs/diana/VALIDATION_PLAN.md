# Validation Plan — True Structure Mission Assurance Platform

**Version:** 1.0  
**Date:** 2026-06-08  
**Classification:** Unclassified / Public  

---

## 1. Purpose

This document defines the validation approach for demonstrating that the True Structure Mission Assurance Platform meets TRL 4 criteria through a reproducible end-to-end demonstration. Validation is achieved through five structured scenarios executed against a defined demonstration dataset, supported by an automated test suite (97/97 tests passing) and an interactive demo script.

---

## 2. Validation Environment

| Item | Specification |
|------|--------------|
| Deployment | Local Docker Compose or cloud (Railway + Vercel) |
| Database | PostgreSQL 16 |
| Backend | FastAPI on Python 3.12 |
| AI provider | Mock (deterministic) — no external API keys required |
| Storage | Local filesystem |
| Dataset | Defense-autonomy sample (`samples/defense-autonomy/`) |
| Demo loader | `make seed-demo` or `apps/api/scripts/demo_flow.py` |

The validation environment is self-contained and reproducible. All expected outcomes are deterministic when using the mock AI provider and the defense-autonomy sample dataset.

---

## 3. Demo Dataset — Autonomous Reconnaissance Sensor Platform

The validation dataset simulates an Autonomous Reconnaissance Sensor Platform (ARSP) program with intentional gaps that demonstrate the platform's detection and reporting capabilities.

### Requirements (REQ-001 to REQ-008)

| ID | Title | Criticality | Category |
|----|-------|-------------|----------|
| REQ-001 | GPS-denied navigation | Critical | Safety |
| REQ-002 | Payload stabilisation | High | Functional |
| REQ-003 | Sensor disagreement handling | Critical | Safety |
| REQ-004 | Fail-safe return | High | Safety |
| REQ-005 | Reject unauthorised commands | Critical | Security |
| REQ-006 | Recover after communication restored | High | Functional |
| REQ-007 | Operator-visible status indicator | Medium | Functional |
| REQ-008 | Validation log | Medium | Functional |

### Test Cases (T-001 to T-005)

| ID | Title | Status | Linked Requirement |
|----|-------|--------|--------------------|
| T-001 | GPS denial flight test | Passed | REQ-001 |
| T-002 | Payload stabilisation test | Passed | REQ-002 |
| T-003 | Fail-safe return test | Passed | REQ-004 |
| T-004 | Sensor disagreement simulation | **Failed** | REQ-003 |
| T-005 | Communication recovery test | Passed | REQ-006 (partial) |

T-004 is intentionally failed to trigger gap detection and score caps.

### Evidence Records (5 records)

Evidence records are associated with T-001 through T-005 test runs, covering functional testing and ArduPilot SITL simulation results.

### Intentional Gaps

- REQ-005 has no security-type test case (triggers `missing_security_validation`)
- REQ-003 has a failed test (T-004) (triggers `failed_test`)
- REQ-006 has no approved test link (triggers `missing_test`)
- REQ-007 and REQ-008 have no approved test links (trigger `missing_test`)

---

## 4. Validation Scenarios

### Scenario 1: Complete Assurance Chain

**Objective:** Verify that requirements, test cases, and evidence can be loaded and linked.

**Input:**
- `samples/defense-autonomy/requirements.md` — 8 requirements
- `samples/defense-autonomy/test_cases.csv` — 5 test cases
- `samples/defense-autonomy/evidence.json` — 5 evidence records

**Expected Outcomes:**

| Check | Expected Value |
|-------|---------------|
| Requirements created | >= 8 |
| Test cases created | >= 5 |
| Evidence records imported | >= 5 |
| API response code (creation) | 201 Created |

**Verification:** Query `GET /api/v1/requirements`, `GET /api/v1/test-cases`, `GET /api/v1/evidence` — counts must match expected values.

---

### Scenario 2: Gap Detection

**Objective:** Verify that the gap detection engine correctly identifies missing coverage, failed tests, and missing security validation.

**Input:** All linked requirements and test cases from Scenario 1.

**Expected Outcomes:**

| Check | Expected Value |
|-------|---------------|
| Total gaps detected | >= 3 |
| Critical + High severity gaps | >= 2 |
| REQ-005 gap type | `missing_security_validation` (Critical) |
| REQ-003 gap type | `failed_test` (Critical) |
| REQ-006 gap type | `missing_test` (High) |

**Verification:** `POST /api/v1/gaps/detect` → `GET /api/v1/gaps`. Verify gap types, severities, and linked requirement IDs.

---

### Scenario 3: Readiness Scoring

**Objective:** Verify that the readiness score is calculated correctly and that score caps are applied as expected.

**Input:** All data from Scenarios 1 and 2.

**Expected Outcomes:**

| Check | Expected Value |
|-------|---------------|
| Overall readiness score | 50–85 (target approximately 61) |
| Score caps applied | >= 2 caps |
| Cap: >30% requirements lack tests | Applied — max 79 |
| Cap: Critical linked test failed | Applied — max 74 |
| Readiness category | "Needs remediation — significant gaps" |

**Verification:** `POST /api/v1/readiness/calculate` → verify `overall_score`, `caps_applied`, and `recommended_actions` fields.

---

### Scenario 4: ATVP Integration

**Objective:** Verify that ATVP-exported evidence can be imported and integrated into the assurance chain.

**Input:** `samples/defense-autonomy/gps_denial_scenario.json` (ATVP JSON export)

**Expected Outcomes:**

| Check | Expected Value |
|-------|---------------|
| Evidence records created | 2 (GPS_DENIAL_001 and GPS_DENIAL_002) |
| Test run GPS_DENIAL_001 | Failed status (GPS lock not recovered) |
| Evidence visible in project | Yes — queryable via `GET /api/v1/evidence` |
| Linked gap created | Yes — linked to REQ-001 or navigation requirement |

**Verification:** `POST /api/v1/atvp/import` → verify response contains created evidence IDs, re-run gap detection, confirm ATVP-derived gap appears.

---

### Scenario 5: Report Generation

**Objective:** Verify that a complete certification readiness report can be generated and downloaded.

**Input:** Full project state after Scenarios 1–4.

**Expected Outcomes:**

| Check | Expected Value |
|-------|---------------|
| Report contains heading | `# Certification Readiness Report` |
| Report references REQ-001 | Yes |
| Report references T-001 | Yes |
| Report contains disclaimer | Yes — AI-assisted disclaimer text |
| Download Content-Type | `text/markdown` |
| HTTP status | 200 OK |

**Verification:** `POST /api/v1/reports/generate` → `GET /api/v1/reports/{id}/download`. Inspect response headers and body for required content.

---

## 5. Automated Test Suite

The automated golden demo test suite provides full regression coverage of all five validation scenarios.

| Item | Detail |
|------|--------|
| File | `apps/api/tests/test_golden_demo.py` |
| Test count | 97 tests |
| Status | 97/97 passing |
| Execution | `make backend-test` or `pytest apps/api/tests/test_golden_demo.py -v` |
| Coverage | Full end-to-end flow: user creation → project → requirements → test cases → evidence → trace links → gap detection → readiness scoring → report generation |

The test suite uses the mock AI provider and an in-memory or test database, producing deterministic results on every run.

---

## 6. Manual Demo Execution

For interactive demonstration to evaluators, the platform provides a 9-step demo script.

| Item | Detail |
|------|--------|
| File | `apps/api/scripts/demo_flow.py` |
| Execution | `python apps/api/scripts/demo_flow.py` |
| Duration | Approximately 5 minutes |
| Steps | 1. Create user and authenticate → 2. Create project → 3. Import requirements → 4. Import test cases → 5. Import evidence → 6. Approve trace links → 7. Run gap detection → 8. Calculate readiness score → 9. Generate and download report |
| Output | Console output with API responses and summary table at each step |

The demo script can also be loaded by running `make seed-demo` to populate the database, then navigating the frontend at `http://localhost:3000`.
