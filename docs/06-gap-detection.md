# Gap Detection

Gap detection is a fully deterministic process. It takes the current project state as input and applies 7 rules. The same input always produces the same gaps. No AI is involved in gap detection.

Gap detection is triggered by the user via `POST /api/v1/projects/{project_id}/gaps/detect`.

---

## Rule 1: Missing Test

**Condition:** A requirement has no approved trace link to any test case.

**Gap type:** `missing_test`

**Severity mapping:**
| Requirement criticality | Gap severity |
|------------------------|--------------|
| catastrophic | critical |
| critical | critical |
| high | high |
| medium | medium |
| low | low |

**Recommendation:** "Add a test case that directly verifies this requirement and create an approved trace link."

---

## Rule 2: Missing Evidence

**Condition:** A requirement has at least one approved trace link to a test case, but that test case has no test runs (evidence).

**Gap type:** `missing_evidence`

**Severity mapping:** Same as Rule 1.

**Recommendation:** "Execute the linked test case and import the test run evidence."

---

## Rule 3: Failed Test

**Condition:** A requirement has an approved trace link to a test case, and the latest test run for that test case has status `failed`.

**Gap type:** `failed_test`

**Severity:** Always one level above the requirement criticality (e.g. high requirement → critical gap), minimum high.

**Recommendation:** "Investigate and resolve the test failure for [test case title]. Re-run and import updated evidence."

---

## Rule 4: Missing Security Validation

**Condition:** A requirement with `category = security` has no approved trace link to a test case with `test_type = security` or `test_type = penetration` or `test_type = static_analysis`.

**Gap type:** `missing_security_validation`

**Severity:** Always critical for requirements with criticality high or above.

**Recommendation:** "Add a dedicated security validation test (penetration test, static analysis or security functional test) for this security requirement."

---

## Rule 5: Missing Safety Validation

**Condition:** A requirement with `category = safety` has no approved trace link to a test case with `test_type = safety`, `test_type = system`, or `test_type = simulation`.

**Gap type:** `missing_safety_validation`

**Severity:** Always critical for requirements with criticality high or above.

**Recommendation:** "Add a safety validation test (system test or simulation) specifically targeting this safety requirement."

---

## Rule 6: Stale Evidence

**Condition:** The most recent test run evidence for a linked test case is older than the staleness threshold for the requirement's criticality level.

**Staleness thresholds:**
| Criticality | Maximum evidence age |
|-------------|---------------------|
| low | 365 days |
| medium | 180 days |
| high | 90 days |
| critical | 30 days |
| catastrophic | 30 days |

**Gap type:** `stale_evidence`

**Severity:** high for critical/catastrophic requirements, medium otherwise.

**Recommendation:** "Re-run [test case title] to produce fresh evidence. Current evidence is [N] days old (threshold: [T] days for [criticality] requirements)."

---

## Rule 7: Unapproved AI Suggestion

**Condition:** A requirement has trace links, but all of them are AI-suggested and none have been reviewed (human_review_status = pending for all links).

**Gap type:** `unapproved_ai_suggestion`

**Severity:** medium

**Recommendation:** "Review the AI-suggested trace links for this requirement and approve or reject them. Unapproved AI suggestions do not count toward coverage."

---

## Gap Severity Summary

| Severity | Meaning for readiness |
|----------|----------------------|
| critical | Triggers score cap — score cannot exceed 74 |
| high | Significant reduction to coverage score |
| medium | Moderate reduction |
| low | Minor reduction |

---

## Gap Status Lifecycle

```
open  →  acknowledged  →  resolved
```

- `open` — newly detected, requires attention
- `acknowledged` — engineer has noted the gap, work in progress
- `resolved` — gap has been addressed (re-run gap detection to confirm)

When gap detection is re-run, existing gaps are compared to new results. Resolved gaps that reappear are set back to `open`.
