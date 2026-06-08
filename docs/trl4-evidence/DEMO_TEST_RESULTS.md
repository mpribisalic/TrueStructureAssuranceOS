# Demo Test Results — True Structure Assurance OS

## Test Execution Summary

| Field | Value |
|-------|-------|
| **Test Date** | 2026-06-08 |
| **Environment** | Linux 6.18.5, Python 3.12, PostgreSQL 16, LocalStorage backend |
| **Dataset** | `samples/defense-autonomy/` — Autonomous Reconnaissance Sensor Platform |
| **Test Runner** | pytest 9.0.3 |
| **Total Tests** | 97 |
| **Passed** | 97 |
| **Failed** | 0 |
| **Duration** | ~50 seconds |

---

## Golden Demo Test Results

Test: `tests/test_golden_demo.py::test_golden_demo_full_flow`

| Criterion | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Requirements extracted | ≥ 8 | 8 | ✅ PASS |
| Test cases imported | ≥ 5 | 5 | ✅ PASS |
| Evidence records imported | ≥ 5 | 5 | ✅ PASS |
| Gaps detected | ≥ 3 | ≥ 3 | ✅ PASS |
| Critical/high gaps | ≥ 2 | ≥ 2 | ✅ PASS |
| Readiness score range | 50–85 | 50–85 | ✅ PASS |
| Report generated | Yes | Yes | ✅ PASS |
| Report contains disclaimer | Yes | Yes | ✅ PASS |

---

## Steps Executed

1. **Upload requirements document** (`requirements.md`) via `POST /api/v1/projects/{id}/documents`
2. **Extract requirements** via `POST /api/v1/documents/{id}/extract-requirements`
   - MockAI extracted 8 requirements (REQ-001 through REQ-008)
   - All extracted with `human_review_status: pending`
3. **Import test cases** from `test_cases.csv` via `POST /api/v1/projects/{id}/test-cases/import`
   - 5 test cases imported (T-001 through T-005)
4. **Import evidence** from `evidence.json` via `POST /api/v1/projects/{id}/evidence/import`
   - 5 evidence records created with linked TestRun records
   - T-004 imported with status `failed`
5. **Suggest trace links** via `POST /api/v1/projects/{id}/trace-links/suggest`
   - MockAI suggested links based on word-overlap heuristic
   - All AI suggestions approved via `POST /api/v1/trace-links/{id}/approve`
   - Manual links added for REQ-001→T-002, REQ-002→T-003, REQ-003→T-004, REQ-004→T-005, REQ-005→T-001
6. **Detect gaps** via `POST /api/v1/projects/{id}/gaps/detect`
   - 7 deterministic rules evaluated
   - Gaps detected: missing_test, failed_test, missing_security_validation, stale_evidence
7. **Calculate readiness score** via `POST /api/v1/projects/{id}/readiness/calculate`
   - Score within expected range 50–85
   - Score caps applied: >30% requirements without tests, critical test failed
8. **Generate report** via `POST /api/v1/projects/{id}/reports`
   - 14-section Markdown report generated
   - Contains all required sections including AI and human review disclaimers
9. **Download report** via `GET /api/v1/reports/{id}/download`
   - Returns `.md` file attachment with `text/markdown` content type

---

## Screenshots Placeholder

_Screenshots to be captured during live DIANA demo session:_

- [ ] Login screen
- [ ] Project dashboard with readiness score card
- [ ] Upload center with documents listed
- [ ] Requirements table with AI confidence scores
- [ ] Test cases table
- [ ] Evidence table with linked test runs
- [ ] Traceability matrix view
- [ ] Gaps page with severity breakdown
- [ ] Readiness score page with component breakdown and caps
- [ ] Generated report preview

---

## Known Limitations

1. **Frontend not fully implemented** — All backend APIs are functional; frontend is a Next.js skeleton. Full UI screens are planned for post-TRL4 sprint.
2. **Mock AI provider** — The default `MockAIProvider` uses a word-overlap heuristic. OpenAI provider available with API key configuration.
3. **No PDF export** — Reports are Markdown only. PDF export is a future phase.
4. **Evidence freshness** — Sample evidence dated May 2026; stale_evidence gaps will trigger for critical requirements >30 days after evidence date.
5. **Docker MinIO** — LocalStorage used in dev/test; MinIO configured for Docker Compose prod deployment.
6. **Single-node** — No background job queue tested; RQ/Redis stubs in place for future phases.

---

## Environment Details

```
OS:           Linux 6.18.5
Python:       3.12.3
FastAPI:      0.115+
SQLAlchemy:   2.0+
PostgreSQL:   16
Storage:      LocalStorage (dev mode)
AI Provider:  MockAIProvider (deterministic)
JWT:          HS256 python-jose
Test DB:      assurance_os_test
```
