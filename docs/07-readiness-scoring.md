# Readiness Scoring

Readiness scoring is fully deterministic. The same project state always produces the same score.

---

## Formula

```
readiness =
  0.30 × coverage_score
+ 0.25 × test_pass_score
+ 0.20 × evidence_score
+ 0.10 × risk_score
+ 0.10 × freshness_score
+ 0.05 × human_review_score
```

All component scores are 0–100. The weighted sum is also 0–100 before caps.

---

## Component Definitions

### coverage_score (30%)
Percentage of active requirements that have at least one **approved** trace link to a test case.

```
coverage_score = (requirements_with_approved_test_link / total_active_requirements) × 100
```

If there are no requirements, coverage_score = 0.

### test_pass_score (25%)
Percentage of requirements where the linked test case has a **passing** test run.

```
test_pass_score = (requirements_with_passing_test_run / requirements_with_approved_test_link) × 100
```

If no requirements have test links, test_pass_score = 0.

### evidence_score (20%)
Percentage of active requirements that have at least one piece of evidence (test run with a result).

```
evidence_score = (requirements_with_evidence / total_active_requirements) × 100
```

### risk_score (10%)
Percentage of identified risks that are mitigated or accepted.

```
risk_score = (mitigated_or_accepted_risks / total_risks) × 100
```

If there are no risks recorded, risk_score = 100 (no known risks).

### freshness_score (10%)
Percentage of evidence items that are within the staleness threshold for their requirement's criticality level.

```
freshness_score = (fresh_evidence_items / total_evidence_items) × 100
```

Thresholds: low=365d, medium=180d, high=90d, critical/catastrophic=30d.

If there is no evidence, freshness_score = 0.

### human_review_score (5%)
Percentage of AI-generated suggestions (requirements + trace links) that have been reviewed by a human.

```
human_review_score = (reviewed_ai_items / total_ai_items) × 100
```

If there are no AI-generated items, human_review_score = 100.

---

## Score Caps

After the weighted formula, caps are applied in order. Each cap limits the maximum possible score.

| Cap condition | Maximum score |
|--------------|---------------|
| Any catastrophic requirement has no approved test link | 59 |
| Any critical safety requirement has no evidence | 69 |
| Any critical security requirement has no evidence | 69 |
| Any critical linked test has failed | 74 |
| More than 30% of requirements lack test links | 79 |
| No evidence exists at all | 49 |
| All trace links are AI-suggested and none approved | 69 |

Multiple caps can apply simultaneously. The lowest cap wins.

**Example:** Project has a catastrophic requirement with no test AND no evidence at all. Caps triggered: 59 and 49. Final maximum: 49.

---

## Score Interpretation

| Score range | Category | Meaning |
|-------------|----------|---------|
| 90–100 | Mission Ready | Strong evidence coverage, no critical gaps |
| 75–89 | Nearly Ready | Minor gaps, small actions required |
| 60–74 | Needs Work | Significant gaps, prioritized remediation needed |
| 45–59 | Not Ready | Critical gaps, substantial work required |
| 0–44 | Blocked | Fundamental gaps, not suitable for evaluation |

---

## Score Output

Every ReadinessScore record includes:

- `overall_score` — final score after caps
- All component scores
- `caps_applied_json` — list of triggered caps with their thresholds
- `top_blockers_json` — top 5 gaps sorted by severity
- `recommended_actions_json` — prioritized action list
- `explanation` — natural language explanation of the score

### Example explanation

```
Readiness score: 62/100 (Needs Work)

Coverage: 62.5% — 5 of 8 requirements have approved test links.
Test pass rate: 80% — 1 of 5 linked tests failed (T-004 sensor disagreement simulation).
Evidence: 50% — 4 of 8 requirements have test run evidence.
Risk: 100% — No open risks recorded.
Freshness: 100% — All evidence is within thresholds.
Human review: 100% — All AI suggestions reviewed.

Caps applied:
- Critical linked test failed (T-004): max score capped at 74.
- More than 30% requirements lack test links: max score capped at 79.
Applied cap: 74. Weighted score before cap: 71 → final score: 62.

Top blockers:
1. REQ-005 (security, high) — missing security validation evidence
2. REQ-003 (safety, high) — linked test T-004 failed
3. REQ-006 (functional, medium) — no test coverage
4. REQ-007 (operational, medium) — no evidence
5. REQ-008 (operational, low) — no validation log evidence
```
