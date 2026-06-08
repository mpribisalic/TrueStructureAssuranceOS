# Technical Validation Plan

**Product:** True Structure Assurance OS
**Date:** 2026-06-08

---

## Validation Approach

TRL 4 validation is based on three levels:

1. **Unit and integration tests** — automated pytest suite covering all core behaviors
2. **Golden demo test** — end-to-end test with defense-autonomy sample dataset
3. **Manual demo validation** — human-run demo following the 5-minute demo script

All automated tests run without internet access using the mock AI provider.

---

## Automated Test Coverage

| Test | What is validated | Expected result |
|------|------------------|----------------|
| `test_health` | API starts, /health returns 200 | `{"status": "ok"}` |
| `test_db_connection` | PostgreSQL reachable, migrations run | No errors |
| `test_project_crud` | Create, read, update, delete project | 201/200/200/204 |
| `test_document_upload` | Upload, hash, store, extract text | Document record with extracted_text |
| `test_requirement_extraction` | Mock AI extracts 8 requirements from sample text | 8 requirement records |
| `test_requirement_approve` | Approve sets human_review_status=approved | Status updated |
| `test_requirement_reject` | Reject sets human_review_status=rejected | Status updated |
| `test_testcase_csv_import` | Import 5 test cases from CSV | 5 TestCase records |
| `test_testcase_csv_invalid` | Reject rows with missing required fields | Error list returned |
| `test_evidence_json_import` | Import 5 evidence items, create TestRuns | 5 TestRun + 5 Evidence records |
| `test_trace_suggestion` | Mock AI suggests 5 links for sample data | 5 TraceLink records (pending) |
| `test_trace_approve` | Approve link changes status | human_review_status=approved |
| `test_trace_reject` | Reject link changes status | human_review_status=rejected |
| `test_gap_missing_test` | Requirement with no trace link → missing_test gap | Gap created |
| `test_gap_missing_evidence` | Requirement linked but no test run → missing_evidence gap | Gap created |
| `test_gap_failed_test` | Test run failed → failed_test gap | Gap created |
| `test_gap_missing_security` | Security req with no security test → gap | Gap created |
| `test_gap_missing_safety` | Safety req with no safety test → gap | Gap created |
| `test_gap_stale_evidence` | Evidence older than threshold → stale_evidence gap | Gap created |
| `test_gap_unapproved_ai` | All links pending → unapproved_ai_suggestion gap | Gap created |
| `test_score_formula` | Formula produces correct weighted result | Score within ±0.1 |
| `test_score_cap_no_test` | Catastrophic req with no test → max 59 | Score ≤ 59 |
| `test_score_cap_no_evidence` | No evidence → max 49 | Score ≤ 49 |
| `test_score_cap_failed_test` | Critical test failed → max 74 | Score ≤ 74 |
| `test_score_cap_low_coverage` | >30% reqs without tests → max 79 | Score ≤ 79 |
| `test_report_generation` | Report contains all required sections | All sections present |
| **`test_golden_demo`** | **Full end-to-end with defense-autonomy dataset** | **See below** |

### Golden Demo Test Assertions

```
requirements_count >= 8
test_cases_count >= 5
gaps_count >= 3
readiness_score >= 50
readiness_score <= 85
critical_or_high_gaps >= 2
report_generated == True
report_contains_disclaimer == True
```

---

## Manual Validation

See `docs/trl4-evidence/DEMO_TEST_RESULTS.md` for manual validation results.

Manual validation follows `docs/11-demo-script.md`.

---

## Known Limitations at TRL 4

1. Mock AI returns fixed results — not a measure of real AI accuracy
2. OpenAI provider not tested with real classified or sensitive data
3. PDF extraction does not handle scanned documents (no OCR)
4. No performance testing beyond single-user demo scenarios
5. MinIO not tested with very large files (>100 MB)
6. Frontend tests are minimal (smoke tests only)
7. No penetration testing performed
8. No formal security audit
