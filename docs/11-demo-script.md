# Demo Script — 5 Minutes

This is the recommended demo flow for NATO DIANA evaluation or stakeholder presentations.

## Setup (before demo)

```bash
make reset
make seed-demo
```

Login: `demo@assuranceos.local` / `demo1234`

---

## Step 1 — Login and Dashboard (30 seconds)

1. Open http://localhost:3000
2. Log in with demo credentials
3. Show the Projects list — one project: "Autonomous Reconnaissance Sensor Platform"
4. **Say:** "This is a dual-use autonomous sensor platform. Our platform ingests its engineering artifacts and tells us if it's ready for certification or deployment."

---

## Step 2 — Requirements (45 seconds)

1. Open the project → Requirements tab
2. Show the 8 structured requirements extracted from the requirements document
3. Point to REQ-005 (security) — highlight the category and criticality
4. Show the AI confidence score and source reference
5. **Say:** "These requirements were extracted by AI from an unstructured Markdown document. Each one has a confidence score. The engineer approved them — AI never certifies anything on its own."

---

## Step 3 — Test Cases and Evidence (45 seconds)

1. Open Test Cases tab — show 5 test cases (T-001 through T-005)
2. Open Evidence tab — show 5 evidence items, highlight T-004 as FAILED
3. **Say:** "Test cases were imported from a CSV. Evidence came from a JSON export of the test execution environment. T-004 — sensor disagreement simulation — failed. That's real data."

---

## Step 4 — Traceability Matrix (45 seconds)

1. Open Traceability tab
2. Show the matrix — requirements linked to test cases
3. Point to REQ-005 — no test coverage shown
4. Point to REQ-006 — no test coverage
5. **Say:** "The AI suggested these links. Engineers approved them. REQ-005 and REQ-006 have no test coverage — the AI could not find matching tests because they don't exist yet."

---

## Step 5 — Gap Detection (45 seconds)

1. Open Gaps tab
2. Show gaps grouped by severity
3. Point to the critical gaps — REQ-005 missing security validation, REQ-003 failed test
4. **Say:** "This is deterministic — not AI. The same rules run every time. No hallucinations. REQ-005 is a security requirement with no security test. That's a critical gap. T-004 failed — that's a critical gap. These block certification."

---

## Step 6 — Readiness Score (30 seconds)

1. Open Readiness tab
2. Show the score gauge — expected 50–85
3. Point to the score caps applied — "critical linked test failed: max 74"
4. Show the top blockers list
5. **Say:** "The score is capped because a critical test failed. The formula is documented, auditable and deterministic. An evaluator can follow the exact calculation."

---

## Step 7 — Report (30 seconds)

1. Open Reports tab
2. Generate a new report
3. Show the Markdown report — scroll through sections
4. Point to the AI disclaimer at the bottom
5. **Say:** "The report is ready for an evaluator, auditor or safety authority. It includes the full traceability matrix, every gap, the score explanation, and a disclaimer that this is AI-assisted — not a formal certification."

---

## Closing (30 seconds)

"In 5 minutes we went from raw artifacts to an explainable readiness report with identified gaps and a prioritized action list. This is what True Structure Assurance OS does — it turns fragmented engineering evidence into mission readiness intelligence."

---

## Key Messages for DIANA Evaluation

- **Trusted autonomy:** Every AI action is logged, explainable, and requires human review
- **Deterministic core:** Gap detection and scoring are pure logic — auditable and reproducible
- **Defense-ready:** Works with disconnected/offline systems (mock AI, local infrastructure)
- **Dual-use:** Same platform works for aerospace, medical, railway, industrial automation
- **TRL 4 validated:** Working prototype with automated test evidence
