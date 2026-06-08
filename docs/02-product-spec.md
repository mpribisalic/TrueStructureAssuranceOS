# Product Specification

## Problem

Defense and regulated engineering teams produce fragmented artifacts across Jira, Confluence, SharePoint, Word, PDF, Excel, GitHub, CI/CD pipelines and local folders.

This makes it impossible to quickly answer:

- Which requirements are covered by tests?
- Which tests have passing evidence?
- Which safety or security requirements are unvalidated?
- What blocks certification readiness?
- What can be shown to an evaluator or auditor today?

Manual review is slow, expensive and error-prone. Verification and validation for safety-critical systems can consume 30–60% of project cost.

## Solution

True Structure Assurance OS ingests the artifacts and produces an evidence graph:

```
Requirement → TestCase → TestRun → Evidence → Gap → ReadinessScore → Report
```

The platform combines AI-assisted extraction with deterministic gap detection and scoring, plus human review at every AI step.

## Scope — TRL 4 Prototype

### Included

| Feature | Description |
|---------|-------------|
| Authentication | JWT login, roles (admin/engineer/viewer) |
| Projects | Create and manage assurance projects per system |
| Document upload | Upload requirements, test cases, evidence, risk assessments |
| Text extraction | Extract text from txt, md, csv, json, pdf, docx |
| Requirement extraction | AI-assisted extraction with human review |
| Test case import | CSV import with validation |
| Evidence import | JSON import linking test runs to test cases |
| Traceability linking | AI-suggested links with human approval/rejection |
| Gap detection | 7 deterministic rules detecting coverage gaps |
| Readiness scoring | Weighted formula with score caps and explanation |
| Dashboard | Cards showing readiness, coverage, gaps, blockers |
| Report generation | Markdown readiness report with disclaimer |
| Audit trail | Full log of all important actions |
| Sample dataset | Defense-autonomy demo dataset with 8 requirements |
| Automated tests | Backend tests proving all core behaviors |
| Local deployment | Docker Compose one-command startup |

### Excluded (future)

- Billing and subscription management
- Enterprise SSO / SAML
- Full RBAC with custom permission sets
- Kubernetes / Helm deployment
- Real classified data handling
- Deep integrations (Jira, Confluence, SharePoint)
- Full compliance library (DO-178C, IEC 62304, EN 50128)
- Advanced graph database
- Real-time telemetry ingestion
- Model fine-tuning
- Formal regulatory certification claims

## User Roles

| Role | Permissions |
|------|-------------|
| admin | Full access, user management |
| engineer | Create/edit projects, upload, review AI suggestions, approve/reject |
| viewer | Read-only access to projects and reports |

## Industry Scope

The platform is intentionally multi-sector:

| Sector | Example use case |
|--------|-----------------|
| Defense | Autonomous systems mission readiness |
| Aerospace | DO-178C / DO-254 evidence readiness |
| Medical | IEC 62304 / FDA software validation |
| Railway | EN 50128 safety case evidence |
| Industrial | Functional safety (IEC 61508) evidence |
| Space | ESA / NASA software assurance evidence |
| Robotics | CE/safety certification for collaborative robots |

## Demo Scenario

The TRL 4 demo uses the **Autonomous Reconnaissance Sensor Platform** dataset:

- 8 requirements (safety, security, operational)
- 5 test cases (simulation, system tests)
- 5 evidence items (4 passed, 1 failed)
- Expected: 5+ gaps, readiness score 50–85, report generated

This scenario intentionally includes a failed test (T-004) and missing coverage (REQ-005, REQ-006, REQ-007, REQ-008) to demonstrate gap detection.
