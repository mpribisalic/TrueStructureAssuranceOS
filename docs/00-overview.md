# True Structure Assurance OS — Overview

## What Is This?

True Structure Assurance OS is an AI-assisted certification and mission readiness platform for defense, dual-use and regulated safety-critical engineering teams.

It ingests unstructured engineering artifacts (requirements documents, test case spreadsheets, evidence logs, risk assessments) and produces an explainable readiness report that answers:

- Which requirements are covered by tests?
- Which tests have passing evidence?
- Where are the gaps that block certification or mission readiness?
- What is the current readiness score and why?
- What actions are needed to improve readiness?

## Core Workflow

```
Unstructured artifacts (PDF, Word, CSV, JSON, Markdown)
        ↓
Document upload and text extraction
        ↓
AI-assisted requirement extraction (human review required)
        ↓
Test case import (CSV)
        ↓
Evidence import (JSON)
        ↓
AI-suggested traceability links (human approval required)
        ↓
Deterministic gap detection (7 rules)
        ↓
Deterministic readiness scoring (weighted formula + caps)
        ↓
Explainable readiness report (Markdown)
```

## Key Design Principles

### AI suggests, humans decide
The AI provider extracts requirements and suggests traceability links. It assigns confidence scores and provides reasoning. It never certifies, approves or claims formal compliance. Every AI output requires human review before it contributes to the readiness score.

### Deterministic core
Gap detection and readiness scoring are pure deterministic functions — no AI involved. The same input always produces the same score. This is required for auditability and NATO/DIANA evaluation.

### Explainability at every step
Every score includes an explanation. Every gap includes a recommendation. Every AI suggestion includes a confidence score, source reference and reason. Every action is recorded in the audit trail.

### Security-aware from the start
Documents are untrusted input. The AI pipeline is isolated from system logic. Secrets are environment variables only. JWT authentication protects all endpoints.

## Target Users

| User | Use case |
|------|----------|
| Defense engineering teams | Mission readiness before deployment |
| Aerospace/space suppliers | Certification evidence readiness |
| Medical device teams | Regulatory submission preparation |
| Railway/industrial teams | Safety case evidence management |
| Dual-use startups | Assurance evidence for investor/partner review |
| NATO DIANA applicants | TRL 4+ prototype demonstration |

## NATO DIANA Positioning

This prototype is built to demonstrate TRL 4 (technology validated in lab environment) for NATO DIANA evaluation. It addresses the DIANA challenge areas of trusted autonomy, AI assurance, mission assurance and cyber-physical validation.

See `docs/trl4-evidence/NATO_DIANA_ALIGNMENT.md` for full alignment mapping.
