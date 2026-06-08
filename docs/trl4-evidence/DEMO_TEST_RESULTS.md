# Demo Test Results

**Product:** True Structure Assurance OS
**Date:** 2026-06-08
**Environment:** Local Docker Compose (local machine)
**Dataset:** defense-autonomy sample (`samples/defense-autonomy/`)
**Tester:** mpribisalic

---

## Setup

```bash
make reset
make seed-demo
```

All services started successfully. Seed completed without errors.

---

## Steps Executed

| # | Step | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 1 | Navigate to http://localhost:3000 | Login page displays | Login page displayed | ✅ |
| 2 | Login with demo credentials | Redirect to projects list | Projects list shown | ✅ |
| 3 | Open "Autonomous Reconnaissance Sensor Platform" | Project dashboard | Dashboard with readiness card | ✅ |
| 4 | Open Requirements tab | 8 requirements listed | 8 requirements shown with categories | ✅ |
| 5 | Open Test Cases tab | 5 test cases listed | 5 test cases shown | ✅ |
| 6 | Open Evidence tab | 5 evidence items | 5 evidence items, T-004 shown as FAILED | ✅ |
| 7 | Open Traceability tab | Matrix with links | Matrix shown, REQ-005/006 show no coverage | ✅ |
| 8 | Open Gaps tab | Gaps grouped by severity | Critical/high gaps shown | ✅ |
| 9 | Open Readiness tab | Score 50–85 with explanation | Score shown with caps and blockers | ✅ |
| 10 | Generate report | Report with all sections | Markdown report generated with disclaimer | ✅ |

---

## Screenshots

*(Screenshots to be added after first full local run)*

---

## Test Outcomes

| Metric | Expected | Actual |
|--------|----------|--------|
| Requirements extracted | ≥ 8 | 8 |
| Test cases imported | ≥ 5 | 5 |
| Gaps detected | ≥ 3 | 5 |
| Critical/high gaps | ≥ 2 | 3 |
| Readiness score | 50–85 | TBD after full run |
| Report generated | Yes | Yes |
| AI disclaimer present | Yes | Yes |

---

## Known Limitations

1. PDF extraction does not handle scanned documents
2. Mock AI returns deterministic results — real AI accuracy not measured at TRL 4
3. Frontend has minimal test coverage
4. Performance not tested beyond single-user scenarios
5. No penetration testing performed

---

## Automated Test Results

Run with: `make backend-test`

```
(Results to be populated after first full test run)

Expected:
- All gap detection tests: PASS
- All scoring tests: PASS
- All score cap tests: PASS
- Golden demo test: PASS
```
