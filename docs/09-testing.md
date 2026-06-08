# Testing Strategy

## Philosophy

Tests prove prototype behavior — not just code coverage. Every test maps to an acceptance criterion from the implementation phases.

The test suite must be runnable without internet access, without OpenAI keys, and without external services (using the mock AI provider and test database).

---

## Backend Tests

Run with: `make backend-test` or `cd apps/api && uv run pytest tests/ -v`

### Test categories

| Category | File | What it proves |
|----------|------|---------------|
| Health | `test_health.py` | API starts and health endpoint works |
| Database | `test_db.py` | Database connection and migrations run cleanly |
| Auth | `test_auth.py` | Login, JWT validation, role enforcement |
| Projects | `test_projects.py` | Project CRUD |
| Documents | `test_documents.py` | Upload, text extraction, processing status |
| Requirements | `test_requirements.py` | Extraction, approve/reject workflow |
| Test cases | `test_test_cases.py` | CSV import, validation errors |
| Evidence | `test_evidence.py` | JSON import, test run creation |
| Traceability | `test_traceability.py` | AI suggestion, approve/reject |
| Gap detection | `test_gaps.py` | All 7 gap rules |
| Readiness scoring | `test_scoring.py` | Formula, all score caps |
| Reports | `test_reports.py` | Markdown report generation |
| Golden demo | `test_golden_demo.py` | End-to-end with defense-autonomy dataset |

### Required test coverage

Every gap detection rule must have:
- A test case where the rule triggers
- A test case where the rule does NOT trigger (negative test)

Every score cap must have:
- A test case where the cap applies
- A test case where the cap does not apply

### Golden Demo Test

The golden demo test loads the complete defense-autonomy sample dataset and verifies:

```
requirements >= 8
test_cases >= 5
gaps >= 3
readiness_score >= 50
readiness_score <= 85
critical_or_high_gaps >= 2
report generated successfully
```

This test is the primary acceptance test for TRL 4.

---

## Frontend Tests

Run with: `make frontend-test` or `cd apps/web && npm test`

TRL 4 scope: basic component render tests and API integration smoke tests.

---

## Test Environment Setup

Tests use a separate test database:

```env
DATABASE_URL=postgresql+psycopg://assurance_user:assurance_pass@localhost:5432/assurance_os_test
LLM_PROVIDER=mock
```

Each test module creates its own database state and tears it down after the test.

---

## CI Pipeline

See `infra/ci/` for GitHub Actions workflow.

Pipeline runs on every push:
1. Backend lint (ruff)
2. Backend tests (pytest)
3. Frontend lint (eslint)

Tests must pass before merging to main.
