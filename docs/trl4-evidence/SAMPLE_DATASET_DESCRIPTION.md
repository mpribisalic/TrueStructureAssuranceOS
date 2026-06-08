# Sample Dataset Description

## Dataset: defense-autonomy

**Location:** `samples/defense-autonomy/`

**Scenario:** Autonomous Reconnaissance Sensor Platform (ARSP)

**Description:**
A dual-use autonomous sensor platform used for reconnaissance, remote inspection and critical infrastructure monitoring. The platform is designed for military reconnaissance and dual-use civilian inspection (power lines, pipelines, bridges). It operates autonomously with degraded-mode fallback behaviors.

This dataset is intentionally designed with gaps to demonstrate the gap detection and readiness scoring capabilities of the platform.

---

## Files

| File | Contents |
|------|----------|
| `requirements.md` | 8 structured requirements (safety, security, operational) |
| `user_stories.md` | 3 user stories |
| `test_cases.csv` | 5 test cases covering nominal and degraded scenarios |
| `evidence.json` | 5 evidence items (4 passed, 1 failed) |
| `risk_assessment.md` | 4 identified risks |
| `expected_gaps.md` | Expected gap detection output |
| `expected_readiness.md` | Expected readiness score range |

---

## Requirements (8)

| ID | Category | Criticality | Description |
|----|----------|-------------|-------------|
| REQ-001 | safety | high | Maintain safe operation 30s after positioning signal degradation |
| REQ-002 | safety | high | Detect communication loss within 5s and enter degraded mode |
| REQ-003 | safety | high | Enter safe mode on critical sensor disagreement |
| REQ-004 | functional | medium | Record telemetry during operation |
| REQ-005 | security | high | Reject unauthorized command messages |
| REQ-006 | functional | medium | Recover normal operation after communication restored |
| REQ-007 | operational | medium | Maintain operator-visible status indicator during degraded operation |
| REQ-008 | operational | low | Produce validation log after each test run |

---

## Test Cases (5)

| ID | Type | Automation | Description |
|----|------|-----------|-------------|
| T-001 | system | automated | Baseline nominal operation |
| T-002 | simulation | automated | Positioning degradation — 30s safe operation |
| T-003 | system | automated | Communication loss detection |
| T-004 | simulation | automated | Sensor disagreement safe mode — **INTENTIONALLY FAILS** |
| T-005 | system | automated | Telemetry recording |

---

## Evidence (5)

| Test | Status | Note |
|------|--------|------|
| T-001 | passed | Nominal operation completed |
| T-002 | passed | 35 seconds safe operation confirmed |
| T-003 | passed | Loss detected in 3.8s |
| T-004 | **failed** | Safe mode transition delayed beyond threshold |
| T-005 | passed | Telemetry file generated |

---

## Intentional Gaps

This dataset is designed to produce these gaps:

| Gap | Type | Severity |
|-----|------|---------|
| REQ-005 — no security test | missing_security_validation | critical |
| REQ-003 — T-004 failed | failed_test | critical |
| REQ-006 — no test coverage | missing_test | medium |
| REQ-007 — no evidence | missing_evidence | medium |
| REQ-008 — partial coverage | missing_evidence | low |

---

## Expected Readiness

- Score range: 50–85
- Category: Needs Work / Not Ready
- Primary blockers: REQ-005 (security), T-004 failure, REQ-006 missing test

---

## Usage

```bash
# Load dataset into running system
make seed-demo

# Run golden demo test
cd apps/api && uv run pytest tests/test_golden_demo.py -v
```
