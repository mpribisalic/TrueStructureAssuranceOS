# Expected Readiness — Autonomous Reconnaissance Sensor Platform

## Score Range
- **Expected:** 50–85
- **Category:** Not ready / needs remediation

## Key Factors Affecting Score

### Positive
- 5 of 8 requirements have test cases linked (62.5% coverage)
- 4 of 5 test runs passed (80% pass rate)
- Evidence exists for T-001 through T-005

### Negative (Score Caps)
- T-004 failed → if linked to critical requirement, caps at 74
- Evidence dated May 2026 may be stale for critical requirements (30-day threshold)
- REQ-005 (security) and REQ-006/REQ-007/REQ-008 lack approved test links → >30% without tests → cap at 79
- No security test for REQ-005 → critical security gap

## Expected Score Caps Applied
- `>30% requirements lack tests → max 79`
- `Critical linked test failed → max 74` (if REQ-003 is critical)
- `No evidence → max 49` (only if evidence entirely absent; not the case here)

## Readiness Category Thresholds
| Score | Category |
|-------|----------|
| 90–100 | Ready for TRL 4 assessment |
| 75–89 | Conditionally ready — minor gaps |
| 60–74 | Needs remediation — significant gaps |
| 0–59 | Not ready — critical blockers |
