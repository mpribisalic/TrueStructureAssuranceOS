# AI Explainability Notes

**Product:** True Structure Assurance OS TRL 4 Prototype
**Date:** 2026-06-08

---

## Core Principle

AI in True Structure Assurance OS is a suggestion engine, not a decision maker.

Every AI output:
- Carries a **confidence score** (0.0–1.0)
- Carries a **reason** (natural language explanation)
- Carries a **source reference** (where in the document the suggestion came from)
- Is marked `pending_review` until a human approves or rejects it
- Is recorded in the **audit log**

---

## What AI Does

| AI function | What it produces | Human action required |
|-------------|-----------------|----------------------|
| Requirement extraction | Structured requirements from raw text | Approve or reject each requirement |
| Trace link suggestion | Links between requirements and test cases | Approve or reject each link |
| Gap explanation | Natural language explanation and recommendations | Review and use in remediation |
| Report summary | Executive summary section of report | Review before sharing |

---

## What AI Does NOT Do

- AI does not certify requirements as complete or correct
- AI does not approve trace links
- AI does not claim formal compliance with any standard
- AI does not modify the readiness score directly
- AI does not delete or modify existing records
- AI output with `pending_review` status contributes **nothing** to the readiness score

---

## Confidence Scores

All AI-generated records include an `ai_confidence` field (0.0–1.0):

| Range | Meaning | UI treatment |
|-------|---------|-------------|
| 0.85–1.0 | High confidence | Green indicator |
| 0.65–0.84 | Medium confidence | Yellow indicator |
| 0.0–0.64 | Low confidence | Red indicator — review carefully |

Low-confidence suggestions are always flagged in the UI and never auto-approved.

---

## Source References

Every AI-extracted requirement includes a `source_reference` field pointing to the location in the source document (e.g., `"requirements.md line 4"`). This allows the engineer to quickly verify the suggestion against the original text.

---

## Deterministic vs AI Components

| Component | Type | Notes |
|-----------|------|-------|
| Requirement extraction | AI | Mock or OpenAI, human review required |
| Trace link suggestion | AI | Mock or OpenAI, human review required |
| Gap explanation | AI | Advisory only, not used in score |
| Report summary | AI | Advisory only, reviewed before publishing |
| Gap detection | Deterministic | 7 fixed rules, no AI |
| Readiness scoring | Deterministic | Weighted formula + caps, no AI |
| Score explanation | Deterministic | Generated from formula output |

---

## Audit Log of AI Actions

Every AI call is recorded in `AuditEvent`:

```
action: "ai.requirement_extraction"
entity_type: "document"
entity_id: <document_id>
metadata_json: {
  "provider": "mock",
  "requirements_extracted": 8,
  "average_confidence": 0.89
}
```

This provides a full audit trail of when AI was used, what it produced, and what the human decided.

---

## Mock AI Transparency

The mock AI provider is disclosed in:
- The UI (banner: "Mock AI provider active — results are deterministic")
- Every report generated with the mock provider (footer note)
- The audit log (provider field)

Results from the mock provider are not a measure of real AI capability. They demonstrate the platform workflow and are used for TRL 4 validation with a synthetic dataset.
