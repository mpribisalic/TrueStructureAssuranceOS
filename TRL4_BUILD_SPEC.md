# True Structure Assurance OS
# NATO DIANA TRL 4 Prototype Build Specification

Version: 1.0  
Purpose: Give this document directly to Claude Code, Codex, Cursor Agent, or another LLM coding agent to build a NATO DIANA-ready TRL 4 prototype.

---

## 0. Why This Document Exists

This document defines exactly what must be built to reach a credible **TRL 4 prototype** for NATO DIANA-style evaluation.

The goal is not to build a finished enterprise product.

The goal is to build a **working laboratory-validated prototype** that demonstrates the core technology:

```text
Unstructured engineering artifacts
        ↓
AI-assisted extraction and structuring
        ↓
Requirement → Test → Evidence traceability
        ↓
Gap detection
        ↓
Certification / mission readiness score
        ↓
Explainable readiness report
```

The prototype must be strong enough for:

- NATO DIANA application
- DIANA-style technical screening
- early pilot discussion
- internal innovation pitch
- defense/dual-use demo
- industrial partner validation

---

## 1. NATO DIANA Context

DIANA seeks mature technological solutions for defence and security challenges through public challenge calls. Selected innovators enter the DIANA Accelerator Programme and continue iterating their proposed solution in response to the challenge.

DIANA evaluates solutions based on factors including:

- alignment to the challenge
- validity
- feasibility
- dual-use potential
- coherence
- novelty
- defence/security relevance
- impact
- commercial viability
- adoption potential
- resources and dependencies
- suitability for DIANA

DIANA seeks technology solutions at **TRL 4 and above**. Lower TRL solutions are not considered.

Therefore, this prototype must demonstrate:

```text
Technology validated in a lab/prototype environment.
```

For this project, TRL 4 means:

- working software prototype
- end-to-end demo workflow
- realistic defense/dual-use dataset
- reproducible local deployment
- documented architecture
- deterministic core logic
- AI-assisted but explainable output
- test evidence
- readiness report generated from sample data

---

## 2. Product Name

Working product name:

```text
True Structure Assurance OS
```

Optional product descriptors:

```text
AI Certification Readiness Platform
AI Assurance Intelligence Platform
Evidence Intelligence Platform for Safety-Critical Systems
Readiness Intelligence Layer for Defense and Regulated Industries
```

---

## 3. One-Line Pitch

```text
True Structure Assurance OS turns unstructured engineering artifacts into explainable certification and mission readiness intelligence for defense, dual-use and regulated safety-critical systems.
```

---

## 4. Core Problem

Defense and regulated engineering teams work with fragmented artifacts:

- user stories
- requirements
- test cases
- test results
- simulation outputs
- logs
- telemetry
- risk assessments
- cybersecurity evidence
- approval documents
- audit files
- standards
- engineering notes

These artifacts are often spread across:

- Jira
- Confluence
- SharePoint
- Word
- PDF
- Excel
- CSV
- GitHub/GitLab
- CI/CD pipelines
- emails
- local folders
- internal test tools

This makes it difficult to answer:

- Which requirements are covered?
- Which requirements lack tests?
- Which tests lack evidence?
- Which safety/security requirements are unvalidated?
- Which evidence is stale?
- Which risks remain open?
- What blocks certification readiness?
- What blocks mission/system readiness?
- What can be shown to an evaluator, auditor, customer or defence stakeholder?

The problem is especially important in defense and dual-use systems because:

- deployment risk is high
- cyber-physical failure can be mission-critical
- AI/autonomy requires trust and evidence
- engineering evidence is fragmented
- verification and validation are expensive
- manual review is slow

---

## 5. Solution Summary

True Structure Assurance OS ingests messy engineering artifacts and creates an evidence graph:

```text
Requirement
    ↓ verified by
Test Case
    ↓ executed as
Test Run
    ↓ supported by
Evidence
    ↓ linked to
Risk / Gap
    ↓ contributes to
Readiness Score
    ↓ summarized in
Assurance Report
```

The system combines:

1. AI extraction and suggestions
2. deterministic gap detection
3. deterministic readiness scoring
4. human review workflow
5. evidence traceability
6. audit logging
7. explainable reports

---

## 6. What Must Be Demonstrated for TRL 4

The prototype must demonstrate the following in a laboratory / demo environment:

### 6.1 Functional Demonstration

A user can:

1. Log in.
2. Create or open a project.
3. Upload requirements or user stories.
4. Extract requirements using AI/mock AI.
5. Import test cases.
6. Import evidence/test results.
7. Generate traceability suggestions.
8. Approve/reject traceability links.
9. Run deterministic gap detection.
10. Calculate readiness score.
11. Generate an explainable readiness report.

### 6.2 Technical Demonstration

The system must show:

- working frontend
- working backend
- database persistence
- local Docker deployment
- repeatable demo dataset
- deterministic tests
- API documentation
- architecture documentation
- security-aware design
- AI provider abstraction
- audit trail

### 6.3 NATO/Defense Demonstration

The demo must show a defense/dual-use scenario:

```text
Autonomous Reconnaissance Sensor Platform
```

But the product must not be drone-only.

It must be positioned for:

- defense autonomous systems
- sensor systems
- command software
- robotics
- aerospace
- medical devices
- railway
- industrial automation
- space systems

---

## 7. TRL 4 Evidence Package

The repo must contain a folder:

```text
docs/trl4-evidence/
```

It must contain:

```text
TRL4_READINESS_ASSESSMENT.md
SYSTEM_ARCHITECTURE.md
TECHNICAL_VALIDATION_PLAN.md
DEMO_TEST_RESULTS.md
SAMPLE_DATASET_DESCRIPTION.md
RISK_REGISTER.md
CYBER_SECURITY_DESIGN_NOTES.md
AI_EXPLAINABILITY_NOTES.md
DUAL_USE_POSITIONING.md
NATO_DIANA_ALIGNMENT.md
PILOT_PLAN.md
```

These files must be generated and kept updated.

---

## 8. Product Scope for TRL 4

### 8.1 Must Build

The prototype must include:

- authentication
- project management
- document upload
- text extraction
- requirement extraction
- test case import
- evidence import
- traceability linking
- AI trace suggestions
- human review of AI suggestions
- gap detection
- readiness scoring
- dashboard
- report generation
- audit trail
- sample defense dataset
- automated tests
- local deployment
- documentation

### 8.2 Must Not Build Yet

Do not build:

- billing
- enterprise SSO
- full RBAC
- Kubernetes
- real classified deployment
- complex integrations
- full compliance library
- advanced graph database
- real-time telemetry
- model fine-tuning
- formal regulatory certification claims

---

## 9. Engineering Architecture

### 9.1 Required Stack

Backend:

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- Alembic
- PostgreSQL
- Redis
- RQ or Celery
- MinIO / S3-compatible storage
- pytest
- ruff

Frontend:

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zod
- Recharts

Infrastructure:

- Docker
- Docker Compose
- Makefile
- GitHub Actions or GitLab CI optional

AI:

- provider abstraction
- mock provider required
- OpenAI provider optional
- local/offline provider interface prepared

---

## 10. Repository Structure

Create:

```text
true-structure-assurance-os/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── LICENSE
│
├── docs/
│   ├── 00-overview.md
│   ├── 01-architecture.md
│   ├── 02-product-spec.md
│   ├── 03-api.md
│   ├── 04-data-model.md
│   ├── 05-ai-pipeline.md
│   ├── 06-gap-detection.md
│   ├── 07-readiness-scoring.md
│   ├── 08-security.md
│   ├── 09-testing.md
│   ├── 10-deployment.md
│   ├── 11-demo-script.md
│   ├── 12-nato-diana-alignment.md
│   ├── 13-trl4-validation.md
│   └── trl4-evidence/
│       ├── TRL4_READINESS_ASSESSMENT.md
│       ├── SYSTEM_ARCHITECTURE.md
│       ├── TECHNICAL_VALIDATION_PLAN.md
│       ├── DEMO_TEST_RESULTS.md
│       ├── SAMPLE_DATASET_DESCRIPTION.md
│       ├── RISK_REGISTER.md
│       ├── CYBER_SECURITY_DESIGN_NOTES.md
│       ├── AI_EXPLAINABILITY_NOTES.md
│       ├── DUAL_USE_POSITIONING.md
│       ├── NATO_DIANA_ALIGNMENT.md
│       └── PILOT_PLAN.md
│
├── apps/
│   ├── api/
│   │   ├── pyproject.toml
│   │   ├── alembic.ini
│   │   ├── app/
│   │   ├── migrations/
│   │   ├── scripts/
│   │   └── tests/
│   │
│   └── web/
│       ├── package.json
│       ├── next.config.js
│       ├── tsconfig.json
│       ├── src/
│       └── tests/
│
├── samples/
│   ├── defense-autonomy/
│   ├── aerospace/
│   ├── medical-device/
│   ├── railway/
│   └── industrial-robotics/
│
├── infra/
│   ├── docker/
│   ├── compose/
│   └── ci/
│
└── scripts/
    ├── dev.sh
    ├── reset.sh
    └── seed.sh
```

---

## 11. Environment Support

The prototype must support:

```text
local
test
staging
production
offline
```

Create `.env.example`:

```env
APP_ENV=local
APP_NAME=True Structure Assurance OS
API_HOST=0.0.0.0
API_PORT=8000

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/assurance_os
REDIS_URL=redis://redis:6379/0

OBJECT_STORAGE_PROVIDER=minio
OBJECT_STORAGE_ENDPOINT=http://minio:9000
OBJECT_STORAGE_BUCKET=assurance-os
OBJECT_STORAGE_ACCESS_KEY=minio
OBJECT_STORAGE_SECRET_KEY=minio123
OBJECT_STORAGE_REGION=local

LLM_PROVIDER=mock
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini

JWT_SECRET=change-this-in-production
JWT_EXPIRES_MINUTES=1440

CORS_ORIGINS=http://localhost:3000

MAX_UPLOAD_SIZE_MB=25
ENABLE_AI=true
ENABLE_SIGNUPS=false
```

Rules:

- never hardcode secrets
- mock AI must work without internet
- offline mode must not call external services
- configuration must be centralized
- test environment must be deterministic

---

## 12. Docker Requirements

Create Docker Compose services:

```text
api
web
worker
postgres
redis
minio
```

Acceptance:

```bash
docker compose up --build
```

must start the system.

Required URLs:

```text
API: http://localhost:8000
Frontend: http://localhost:3000
Health: http://localhost:8000/health
```

---

## 13. Makefile Commands

Implement:

```makefile
up
down
reset
logs
backend-test
frontend-test
lint
format
migrate
seed-demo
demo
```

---

## 14. Backend Architecture

Create:

```text
apps/api/app/
├── main.py
├── config.py
├── api/
│   └── v1/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── repositories/
├── documents/
├── ai/
├── scoring/
├── reports/
├── storage/
├── jobs/
└── utils/
```

Rules:

- API routes call services.
- Services contain business logic.
- Repositories contain database access.
- AI providers are replaceable.
- Scoring must be deterministic.
- Gap detection must be deterministic.
- Audit events must be created for important actions.

---

## 15. Core Domain Models

Use UUID primary keys.

All models need timestamps.

### 15.1 Organization

Fields:

```text
id
name
industry
created_at
updated_at
```

### 15.2 User

Fields:

```text
id
organization_id
email
name
password_hash
role
is_active
created_at
updated_at
```

Roles:

```text
admin
engineer
viewer
```

### 15.3 Project

Fields:

```text
id
organization_id
name
description
industry
system_type
criticality_level
status
created_at
updated_at
```

Industry enum:

```text
defense
aerospace
medical
railway
industrial
automotive
space
robotics
energy
other
```

Criticality enum:

```text
low
medium
high
mission_critical
safety_critical
```

### 15.4 Document

Fields:

```text
id
project_id
uploaded_by_user_id
filename
file_type
source_type
storage_uri
file_hash
file_size_bytes
processing_status
extracted_text
processing_error
created_at
updated_at
```

Source type enum:

```text
requirements
user_stories
test_plan
test_cases
test_results
evidence
risk_assessment
standard
log
telemetry
report
other
```

### 15.5 Requirement

Fields:

```text
id
project_id
source_document_id
external_id
title
text
category
criticality
priority
verification_method
status
ai_confidence
source_reference
human_review_status
created_at
updated_at
```

### 15.6 TestCase

Fields:

```text
id
project_id
source_document_id
external_id
title
description
test_type
automation_level
status
created_at
updated_at
```

### 15.7 TestRun

Fields:

```text
id
project_id
test_case_id
external_id
status
executed_at
duration_seconds
environment
result_summary
raw_result_uri
created_at
```

### 15.8 Evidence

Fields:

```text
id
project_id
source_document_id
test_run_id
title
description
evidence_type
storage_uri
hash
created_by_user_id
evidence_date
created_at
updated_at
```

### 15.9 TraceLink

Fields:

```text
id
project_id
source_type
source_id
target_type
target_id
link_type
confidence
reason
created_by
human_review_status
created_at
updated_at
```

### 15.10 Risk

Fields:

```text
id
project_id
title
description
severity
likelihood
risk_level
mitigation_status
related_requirement_id
created_at
updated_at
```

### 15.11 Gap

Fields:

```text
id
project_id
gap_type
title
description
severity
status
related_requirement_id
related_test_case_id
related_evidence_id
ai_confidence
recommendation
created_at
updated_at
```

### 15.12 ReadinessScore

Fields:

```text
id
project_id
overall_score
coverage_score
test_pass_score
evidence_score
risk_score
freshness_score
human_review_score
critical_blocker_count
high_gap_count
medium_gap_count
low_gap_count
explanation
caps_applied_json
top_blockers_json
recommended_actions_json
created_at
```

### 15.13 Report

Fields:

```text
id
project_id
readiness_score_id
title
report_type
format
storage_uri
content_markdown
created_by_user_id
created_at
```

### 15.14 AuditEvent

Fields:

```text
id
project_id
actor_user_id
action
entity_type
entity_id
before_json
after_json
metadata_json
created_at
```

---

## 16. API Endpoints

All endpoints under:

```text
/api/v1
```

### 16.1 Health

```http
GET /health
```

### 16.2 Auth

```http
POST /api/v1/auth/login
GET /api/v1/auth/me
POST /api/v1/auth/logout
```

### 16.3 Projects

```http
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

### 16.4 Documents

```http
POST /api/v1/projects/{project_id}/documents
GET  /api/v1/projects/{project_id}/documents
GET  /api/v1/documents/{document_id}
POST /api/v1/documents/{document_id}/process
```

### 16.5 Requirements

```http
POST /api/v1/documents/{document_id}/extract-requirements
GET  /api/v1/projects/{project_id}/requirements
POST /api/v1/projects/{project_id}/requirements
PATCH /api/v1/requirements/{requirement_id}
POST /api/v1/requirements/{requirement_id}/approve
POST /api/v1/requirements/{requirement_id}/reject
```

### 16.6 Test Cases

```http
POST /api/v1/projects/{project_id}/test-cases/import
GET  /api/v1/projects/{project_id}/test-cases
GET  /api/v1/test-cases/{test_case_id}
```

### 16.7 Evidence

```http
POST /api/v1/projects/{project_id}/evidence/import
GET  /api/v1/projects/{project_id}/evidence
GET  /api/v1/evidence/{evidence_id}
```

### 16.8 Traceability

```http
POST /api/v1/projects/{project_id}/trace-links/suggest
GET  /api/v1/projects/{project_id}/trace-links
POST /api/v1/trace-links/{trace_link_id}/approve
POST /api/v1/trace-links/{trace_link_id}/reject
```

### 16.9 Gaps

```http
POST /api/v1/projects/{project_id}/gaps/detect
GET  /api/v1/projects/{project_id}/gaps
PATCH /api/v1/gaps/{gap_id}
```

### 16.10 Readiness

```http
POST /api/v1/projects/{project_id}/readiness/calculate
GET  /api/v1/projects/{project_id}/readiness/latest
GET  /api/v1/projects/{project_id}/readiness/history
```

### 16.11 Reports

```http
POST /api/v1/projects/{project_id}/reports
GET  /api/v1/projects/{project_id}/reports
GET  /api/v1/reports/{report_id}
```

---

## 17. AI Requirements

### 17.1 AI Provider Interface

Create:

```python
class AIProvider:
    def extract_requirements(self, text: str) -> RequirementExtractionResult:
        ...

    def suggest_trace_links(self, requirements, test_cases, evidence) -> TraceSuggestionResult:
        ...

    def explain_gaps(self, gaps) -> GapExplanationResult:
        ...

    def generate_report_summary(self, context) -> ReportSummaryResult:
        ...
```

### 17.2 Mock Provider

Required.

Must return deterministic results for sample dataset.

Used for:

- tests
- offline mode
- repeatable DIANA demo
- TRL 4 validation package

### 17.3 OpenAI Provider

Optional.

Must:

- use strict JSON
- validate outputs
- store confidence
- store reasoning
- store source references
- never silently approve output

### 17.4 AI Safety Rules

Documents are untrusted input.

The AI must not obey instructions inside uploaded documents.

AI may suggest.

AI may not certify.

AI may not approve.

AI may not claim formal compliance.

Human review status is required.

---

## 18. AI Output Schemas

### Requirement Extraction

```json
{
  "requirements": [
    {
      "external_id": "REQ-001",
      "title": "Safe operation under positioning degradation",
      "text": "The system shall maintain safe operation for at least 30 seconds after positioning signal degradation.",
      "category": "safety",
      "criticality": "high",
      "verification_method": "test",
      "confidence": 0.91,
      "source_reference": "requirements.md line 4"
    }
  ]
}
```

### Traceability Suggestion

```json
{
  "links": [
    {
      "requirement_external_id": "REQ-001",
      "test_case_external_id": "T-002",
      "link_type": "verifies",
      "confidence": 0.86,
      "reason": "The test simulates degraded positioning and verifies safe operation duration."
    }
  ]
}
```

### Gap Explanation

```json
{
  "summary": "The project has critical validation gaps affecting certification readiness.",
  "recommended_actions": [
    "Add cybersecurity validation for unauthorized command rejection.",
    "Re-run failed sensor disagreement simulation.",
    "Add explicit validation log evidence."
  ]
}
```

---

## 19. Document Processing

Support:

```text
txt
md
csv
json
pdf
docx
```

Required:

- file validation
- file size limit
- hash calculation
- storage upload
- text extraction
- extraction errors saved
- processing status updated

Do not use OCR in MVP unless necessary.

---

## 20. Test Case Import

CSV format:

```csv
external_id,title,description,test_type,automation_level,status
```

Validate required fields.

Reject invalid rows with clear errors.

---

## 21. Evidence Import

JSON format:

```json
[
  {
    "external_test_id": "T-001",
    "status": "passed",
    "executed_at": "2026-05-01T10:00:00Z",
    "environment": "simulation",
    "summary": "Nominal operation completed successfully."
  }
]
```

Behavior:

- create TestRun
- create Evidence
- link Evidence to TestRun
- associate with TestCase by external_test_id

---

## 22. Gap Detection Rules

Gap detection must be deterministic.

### Rule 1: Missing Test

If requirement has no approved trace link to a test case:

```text
gap_type = missing_test
```

### Rule 2: Missing Evidence

If requirement has linked test but no evidence/test run:

```text
gap_type = missing_evidence
```

### Rule 3: Failed Test

If linked test run failed:

```text
gap_type = failed_test
```

### Rule 4: Missing Security Validation

If requirement category is security and no linked security test exists:

```text
gap_type = missing_security_validation
```

### Rule 5: Missing Safety Validation

If requirement category is safety and no linked safety/system/simulation test exists:

```text
gap_type = missing_safety_validation
```

### Rule 6: Stale Evidence

Evidence thresholds:

```text
low: 365 days
medium: 180 days
high: 90 days
critical/catastrophic: 30 days
```

### Rule 7: Unapproved AI Suggestion

If traceability depends only on unapproved AI suggestions:

```text
gap_type = unapproved_ai_suggestion
```

---

## 23. Readiness Scoring

Formula:

```text
readiness =
  0.30 * coverage_score
+ 0.25 * test_pass_score
+ 0.20 * evidence_score
+ 0.10 * risk_score
+ 0.10 * freshness_score
+ 0.05 * human_review_score
```

### Score Caps

Apply:

```text
If any catastrophic requirement has no approved test: max 59
If any critical safety requirement has no evidence: max 69
If any critical security requirement has no evidence: max 69
If any critical linked test failed: max 74
If more than 30% requirements lack tests: max 79
If no evidence exists: max 49
If all trace links are AI-suggested and none approved: max 69
```

Readiness output must include:

- overall score
- component scores
- caps applied
- top blockers
- recommended actions
- explanation

---

## 24. Frontend Screens

### Login

Simple login form.

### Projects

Project list with:

- name
- industry
- readiness score
- open gaps
- updated date

### Project Dashboard

Cards:

- readiness score
- requirement coverage
- test pass rate
- evidence completeness
- critical gaps
- top blockers

### Upload Center

Upload:

- requirements
- user stories
- test cases
- evidence
- risk assessment

### Requirements

Table:

```text
External ID
Title
Category
Criticality
Coverage Status
AI Confidence
Human Review Status
Actions
```

### Test Cases

Table:

```text
External ID
Title
Type
Automation Level
Status
```

### Evidence

Table:

```text
Title
Type
Related Test
Date
Status
```

### Traceability Matrix

Table:

```text
Requirement
Test
Evidence
Status
Confidence
Review
```

### Gaps

Grouped by severity:

- critical
- high
- medium
- low

### Readiness

Show:

- score gauge
- components
- caps
- blockers
- recommendations

### Reports

Show generated reports.

Allow report creation.

---

## 25. Defense Demo Dataset

Create:

```text
samples/defense-autonomy/
```

Files:

```text
requirements.md
user_stories.md
test_cases.csv
evidence.json
risk_assessment.md
expected_gaps.md
expected_readiness.md
```

### 25.1 Project

```text
Autonomous Reconnaissance Sensor Platform
```

Description:

```text
A dual-use autonomous sensor platform used for reconnaissance, remote inspection and critical infrastructure monitoring.
```

### 25.2 Requirements

```text
REQ-001: The system shall maintain safe operation for at least 30 seconds after positioning signal degradation.
REQ-002: The system shall detect communication loss within 5 seconds and enter degraded mode.
REQ-003: The system shall enter safe mode when critical sensor disagreement is detected.
REQ-004: The system shall record telemetry during operation for post-run analysis.
REQ-005: The system shall reject unauthorized command messages.
REQ-006: The system shall recover normal operation after communication is restored.
REQ-007: The system shall maintain an operator-visible status indicator during degraded operation.
REQ-008: The system shall produce a validation log after each test run.
```

### 25.3 User Stories

```text
US-001: As an operator, I want the system to continue operating after positioning degradation so that mission interruption is minimized.
US-002: As an operator, I want communication loss detected quickly so that safe fallback behavior occurs.
US-003: As security personnel, I want unauthorized commands rejected so that hostile actors cannot manipulate the system.
```

### 25.4 Test Cases

```csv
external_id,title,description,test_type,automation_level,status
T-001,Baseline operation test,Validates nominal system operation under normal conditions,system,automated,active
T-002,Positioning degradation test,Simulates degraded positioning and checks safe operation for 30 seconds,simulation,automated,active
T-003,Communication loss detection test,Simulates communication loss and validates degraded mode entry,system,automated,active
T-004,Sensor disagreement simulation,Simulates inconsistent sensor values and checks safe mode behavior,simulation,automated,active
T-005,Telemetry recording test,Checks whether telemetry is recorded during operation,system,automated,active
```

### 25.5 Evidence

```json
[
  {
    "external_test_id": "T-001",
    "status": "passed",
    "executed_at": "2026-05-01T10:00:00Z",
    "environment": "simulation",
    "summary": "Nominal operation completed successfully."
  },
  {
    "external_test_id": "T-002",
    "status": "passed",
    "executed_at": "2026-05-01T11:00:00Z",
    "environment": "simulation",
    "summary": "System maintained safe operation for 35 seconds under degraded positioning."
  },
  {
    "external_test_id": "T-003",
    "status": "passed",
    "executed_at": "2026-05-02T09:00:00Z",
    "environment": "simulation",
    "summary": "Communication loss detected in 3.8 seconds."
  },
  {
    "external_test_id": "T-004",
    "status": "failed",
    "executed_at": "2026-05-02T12:00:00Z",
    "environment": "simulation",
    "summary": "Safe mode transition was delayed beyond acceptable threshold."
  },
  {
    "external_test_id": "T-005",
    "status": "passed",
    "executed_at": "2026-05-03T12:00:00Z",
    "environment": "simulation",
    "summary": "Telemetry file was generated and stored."
  }
]
```

### 25.6 Expected Gaps

```text
REQ-005 missing cybersecurity validation evidence.
REQ-003 linked test failed.
REQ-006 missing direct test coverage.
REQ-007 missing evidence.
REQ-008 partially covered but lacks explicit validation log evidence.
```

### 25.7 Expected Readiness

```text
Score range: 50-85
Expected category: Not ready / needs remediation
```

---

## 26. TRL 4 Validation Tests

Create automated tests proving prototype behavior.

### Backend Tests

Required:

- health endpoint test
- database connection test
- project creation test
- document upload model test
- requirement extraction validation test
- test case CSV import test
- evidence JSON import test
- trace suggestion validation test
- gap detection tests
- readiness score formula test
- score cap tests
- report generation test

### Golden Demo Test

Create a test that loads sample defense dataset and verifies:

```text
requirements >= 8
test_cases >= 5
gaps >= 3
readiness_score >= 50
readiness_score <= 85
critical_or_high_gaps >= 2
report generated successfully
```

### Manual Demo Validation

Create:

```text
docs/trl4-evidence/DEMO_TEST_RESULTS.md
```

Include:

- test date
- environment
- dataset used
- steps executed
- screenshots placeholder
- expected result
- actual result
- known limitations

---

## 27. NATO DIANA Alignment Document

Create:

```text
docs/trl4-evidence/NATO_DIANA_ALIGNMENT.md
```

It must include:

### 27.1 Challenge Relevance

Explain that the solution supports:

- trusted autonomy
- mission assurance
- AI assurance
- cyber-physical validation
- defense software readiness
- faster verification and validation

### 27.2 Defence Impact

Explain:

- reduces manual validation burden
- identifies missing evidence
- improves readiness visibility
- supports faster fielding
- improves trust in complex systems

### 27.3 Dual-Use Potential

Map defense to civilian:

```text
Defense autonomy → industrial robotics
Mission assurance → aerospace readiness
Cyber validation → medical/railway safety evidence
Evidence graph → regulated engineering compliance
```

### 27.4 Adoption Path

Initial adopters:

- dual-use startups
- test automation teams
- robotics companies
- defense innovation units
- aerospace suppliers
- regulated engineering teams

### 27.5 Commercial Viability

Business models:

- SaaS
- enterprise license
- on-prem defense deployment
- per-project readiness assessment
- pilot-based consulting-to-product transition

---

## 28. Security Architecture Notes

Create:

```text
docs/trl4-evidence/CYBER_SECURITY_DESIGN_NOTES.md
```

Include:

- authentication
- authorization
- audit trail
- file validation
- safe storage
- no secrets in code
- environment-based secrets
- future on-prem deployment
- future air-gapped deployment
- AI prompt injection risk
- human-in-the-loop AI review

---

## 29. AI Explainability Notes

Create:

```text
docs/trl4-evidence/AI_EXPLAINABILITY_NOTES.md
```

Include:

- AI suggestions include confidence
- AI suggestions include source references
- AI suggestions include reasons
- AI does not certify
- AI does not approve
- human review required
- deterministic scoring separate from AI
- audit log records AI actions

---

## 30. Pilot Plan

Create:

```text
docs/trl4-evidence/PILOT_PLAN.md
```

Pilot stages:

### Pilot 0: Internal Synthetic Validation

Use sample dataset.

Goal:

- prove core workflow
- validate gap detection
- validate readiness score

### Pilot 1: Friendly Engineering Partner

Use anonymized real project artifacts.

Goal:

- compare AI traceability with human review
- measure time saved
- identify missing evidence

### Pilot 2: Dual-Use / Defense-Relevant Partner

Use realistic defense-adjacent data.

Goal:

- validate relevance for mission/certification readiness
- gather adoption feedback

### Pilot 3: Regulated Industry Partner

Use aerospace, medical, railway, or industrial automation data.

Goal:

- prove civil dual-use expansion

Metrics:

- time saved
- gaps found
- traceability precision
- evidence completeness improvement
- user acceptance
- report usefulness

---

## 31. TRL Roadmap

Create:

```text
docs/trl4-evidence/TRL4_READINESS_ASSESSMENT.md
```

Include:

### Current Target: TRL 4

Evidence:

- working lab prototype
- sample dataset
- repeatable demo
- automated tests
- readiness report
- architecture documentation

### TRL 5 Plan

Relevant environment validation:

- pilot with anonymized real engineering data
- real user feedback
- external partner validation
- more realistic evidence imports

### TRL 6 Plan

Operational demonstration:

- pilot with real defense/dual-use team
- workflow embedded in existing validation process
- measurable time savings
- readiness reports used in review process

---

## 32. Report Generation

Generate Markdown report first.

Report sections:

1. Project summary
2. Dataset summary
3. Extracted requirements
4. Test cases
5. Evidence summary
6. Traceability matrix
7. Detected gaps
8. Readiness score
9. Score explanation
10. Top blockers
11. Recommended actions
12. AI usage disclaimer
13. Human review disclaimer
14. Audit trail summary

Disclaimer:

```text
This report is AI-assisted and does not represent formal regulatory certification or approval. All findings must be reviewed by qualified engineering, safety, compliance or mission assurance personnel.
```

---

## 33. Implementation Phases

### Phase 0: Repository Bootstrap

Tasks:

- create monorepo
- create Docker Compose
- create Makefile
- create README
- create docs
- create sample folders
- create backend skeleton
- create frontend skeleton

Acceptance:

```bash
make up
```

starts services.

### Phase 1: Backend Foundation

Tasks:

- FastAPI app
- config
- database
- Alembic
- health endpoint
- logging
- errors
- base models

Acceptance:

```text
GET /health works.
Migrations run.
```

### Phase 2: Auth + Projects

Tasks:

- User
- Organization
- Project
- login
- JWT
- seed demo user
- project CRUD
- frontend login/project list

Acceptance:

User can log in and create/open project.

### Phase 3: Documents

Tasks:

- document upload
- MinIO storage
- text extraction
- processing status
- upload UI

Acceptance:

User uploads requirements file and sees extracted text status.

### Phase 4: Requirement Extraction

Tasks:

- AI interface
- mock AI
- requirement model
- extraction endpoint
- requirement table
- approve/reject/edit

Acceptance:

Sample requirements become structured requirement records.

### Phase 5: Test Cases

Tasks:

- CSV import
- test case model
- test case UI

Acceptance:

Sample test cases imported.

### Phase 6: Evidence

Tasks:

- evidence import
- test run model
- evidence model
- evidence UI

Acceptance:

Sample evidence creates test runs and evidence.

### Phase 7: Traceability

Tasks:

- trace links
- AI suggestions
- approve/reject workflow
- traceability matrix

Acceptance:

User can approve links.

### Phase 8: Gap Detection

Tasks:

- deterministic gap rules
- gap model
- gap page

Acceptance:

Expected gaps appear.

### Phase 9: Readiness

Tasks:

- scoring engine
- score caps
- explanation
- dashboard cards
- readiness page

Acceptance:

Score calculated with blockers.

### Phase 10: Reports

Tasks:

- markdown report
- report model
- report UI
- download/export

Acceptance:

Report generated from sample project.

### Phase 11: TRL 4 Evidence Pack

Tasks:

- generate all docs under docs/trl4-evidence
- run golden demo test
- update validation notes
- update NATO alignment document

Acceptance:

Repository contains complete TRL 4 evidence package.

### Phase 12: Polish and Review

Tasks:

- improve UI
- improve error handling
- improve docs
- run all tests
- fix issues
- prepare 5-minute demo flow

Acceptance:

Prototype is demo-ready.

---

## 34. Recommended Prompt Sequence for Claude Code / Codex

Use one prompt per phase.

### Prompt 1

```text
Read the NATO DIANA TRL 4 Prototype Build Specification. Create the repository skeleton, Docker Compose setup, Makefile, docs structure, FastAPI skeleton, Next.js skeleton, and sample data folders. Do not implement business logic yet. Ensure make up starts the system.
```

### Prompt 2

```text
Implement backend foundation: config, database, Alembic, health endpoint, logging, error handling, base models, and backend test setup. Add tests and update docs.
```

### Prompt 3

```text
Implement authentication, organizations, users, projects, JWT login, seed demo user, project CRUD endpoints, and frontend login/project list/project creation screens. Add tests and update docs.
```

### Prompt 4

```text
Implement document upload with MinIO, file validation, document model, text extraction for txt/md/pdf/docx, processing status, upload UI, and tests.
```

### Prompt 5

```text
Implement AI provider abstraction, mock AI provider, requirement extraction endpoint, requirement model, requirement UI, approve/reject/edit workflow, and tests.
```

### Prompt 6

```text
Implement test case CSV import, test case model, API endpoints, frontend table, validation errors, and tests.
```

### Prompt 7

```text
Implement evidence JSON import, test run model, evidence model, endpoints, frontend evidence screen, and tests.
```

### Prompt 8

```text
Implement traceability links, mock AI trace suggestions, approval/rejection workflow, traceability matrix UI, and tests.
```

### Prompt 9

```text
Implement deterministic gap detection rules, gap model, gap detection endpoint, gap UI grouped by severity, and tests.
```

### Prompt 10

```text
Implement readiness scoring engine with component scores, caps, explanations, dashboard cards, readiness screen, and tests.
```

### Prompt 11

```text
Implement markdown report generation, report model, report endpoint, reports UI, download/export, and tests.
```

### Prompt 12

```text
Create complete defense-autonomy sample dataset, seed-demo script, golden demo test, and demo documentation.
```

### Prompt 13

```text
Create the full TRL 4 evidence package under docs/trl4-evidence, including NATO alignment, validation plan, pilot plan, cybersecurity notes, AI explainability notes, dual-use positioning, risk register, and readiness assessment.
```

### Prompt 14

```text
Review the full codebase for architecture, security, testing, deployment reliability, documentation quality and NATO DIANA TRL 4 demo readiness. Fix issues and list remaining limitations.
```

---

## 35. Definition of Done for NATO DIANA TRL 4 Prototype

The prototype is done when:

1. Fresh clone works.
2. `make up` starts all services.
3. User can log in.
4. User can create/open project.
5. User can upload requirements.
6. System extracts requirements.
7. User can import test cases.
8. User can import evidence.
9. System suggests traceability.
10. User can approve/reject trace links.
11. System detects gaps.
12. System calculates readiness.
13. System generates report.
14. Dashboard shows readiness and blockers.
15. Golden demo test passes.
16. Backend tests pass.
17. Frontend basic tests pass.
18. TRL 4 evidence package exists.
19. NATO alignment document exists.
20. Demo script exists.
21. No secrets committed.
22. AI usage is explainable.
23. Scoring is deterministic.
24. Audit trail exists.
25. Known limitations documented.

---

## 36. Final Instruction to LLM Agent

Build this as a serious prototype for a defense and regulated-industry accelerator application.

Do not build a toy app.

Do not overbuild enterprise features.

Focus on the core evidence workflow:

```text
Requirement → Test → Evidence → Gap → Readiness → Report
```

After each phase:

- run tests
- update docs
- summarize what changed
- list limitations
- propose next step

The objective is a credible TRL 4 prototype, not a final certified product.

