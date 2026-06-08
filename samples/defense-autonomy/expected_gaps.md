# Expected Gaps — Autonomous Reconnaissance Sensor Platform

The following gaps are expected when running gap detection on this dataset.

## GAP-1: REQ-005 Missing Security Validation
- **Type:** missing_security_validation
- **Severity:** Critical
- REQ-005 (reject unauthorized commands) is a security requirement with no linked security-type test case.

## GAP-2: REQ-003 Failed Test
- **Type:** failed_test
- **Severity:** Critical
- T-004 (Sensor disagreement simulation) is the linked test for REQ-003 and has status `failed`.

## GAP-3: REQ-006 Missing Test Coverage
- **Type:** missing_test
- **Severity:** High
- REQ-006 (recover after communication restored) has no test case linked.

## GAP-4: REQ-007 Missing Evidence
- **Type:** missing_test or missing_evidence
- **Severity:** Medium
- REQ-007 (operator-visible status indicator) has no test case linked.

## GAP-5: REQ-008 Partial Coverage
- **Type:** missing_test or missing_evidence
- **Severity:** Medium
- REQ-008 (validation log) has partial coverage but lacks explicit validation log evidence.

## Stale Evidence Note
Evidence from May 2026 may trigger stale_evidence gaps for high/critical criticality requirements
depending on the run date (threshold: 30 days for critical, 90 days for high).
