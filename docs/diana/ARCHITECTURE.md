# True Structure Mission Assurance Platform — Architecture Document

## 1. Executive Summary

The True Structure Mission Assurance Platform is a purpose-built validation and verification intelligence system that transforms unstructured engineering artifacts — requirements documents, test case records, and evidence logs — into explainable certification and mission readiness intelligence. The platform serves both defense and civil regulated-industry customers: on the defense side it supports trusted autonomy programs (UAS, UGV, USV) requiring NATO certification evidence chains, and on the civil side it accelerates DO-178C, ISO 26262, IEC 62304, and IEC 61508 certification cycles. The dual-use architecture comprises two integrated components: the Assurance OS (backend API + web frontend) and the Autonomous Test Validation Platform (ATVP), connected via a deterministic JSON evidence connector.

---

## 2. Platform Architecture

```
TrueStructureAssuranceOS/
├── apps/
│   ├── api/                        # Assurance OS — FastAPI backend
│   │   ├── app/
│   │   │   ├── api/v1/             # REST endpoint routers (14 resource groups)
│   │   │   ├── core/               # Config, security, errors, dependencies
│   │   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── repositories/       # Data access layer
│   │   │   ├── schemas/            # Pydantic request/response schemas
│   │   │   ├── services/           # Business logic
│   │   │   │   ├── ai/             # AI provider abstraction (mock / OpenAI)
│   │   │   │   ├── gap_service.py          # 7-rule deterministic gap detection
│   │   │   │   ├── readiness_service.py    # Weighted scoring + 6 caps
│   │   │   │   ├── report_service.py       # Markdown report generation
│   │   │   │   └── mission_impact_service.py
│   │   │   └── workers/            # Background task workers
│   │   ├── alembic/                # Database migration scripts
│   │   ├── scripts/                # demo_flow.py, seed scripts
│   │   └── tests/                  # pytest suite (97/97 passing)
│   │       └── test_golden_demo.py # End-to-end TRL 4 validation tests
│   └── web/                        # Next.js 15 frontend
│       ├── app/                    # App router pages
│       ├── components/             # React UI components
│       └── lib/                    # API client, utilities
├── atvp/                           # Autonomous Test Validation Platform
│   ├── scenarios/                  # ArduPilot SITL test scenarios (GPS denial, etc.)
│   ├── connectors/                 # JSON export connector for Assurance OS import
│   └── results/                    # Structured test result outputs
├── samples/
│   └── defense-autonomy/           # Demo dataset: Autonomous Reconnaissance Sensor Platform
│       ├── requirements.md
│       ├── test_cases.csv
│       ├── evidence.json
│       └── gps_denial_scenario.json
└── docs/
    ├── diana/                      # NATO DIANA documentation package
    └── deployment/                 # Deployment guides
```

### Component Descriptions

**Assurance OS — FastAPI Backend**
The core backend implements the full assurance chain from requirements ingest through readiness scoring. It exposes a versioned REST API (`/api/v1`) with JWT authentication. Key service modules include: AI provider abstraction (deterministic mock by default, optional OpenAI), a 7-rule deterministic gap detection engine, a 6-cap weighted readiness scoring engine, a Markdown certification report generator, and a mission impact analysis service.

**Assurance OS — Next.js Frontend**
The web interface provides project management, document upload, AI-assisted requirement review, traceability link approval, gap dashboard, readiness score display, and report download. It communicates exclusively with the backend API.

**ATVP — Autonomous Test Validation Platform**
ATVP executes hardware-in-the-loop and software-in-the-loop (ArduPilot SITL) scenarios for autonomous systems. It produces structured JSON test result exports that can be imported into the Assurance OS as evidence records, closing the loop between physical test execution and certification documentation.

---

## 3. Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2, Alembic, pydantic-settings |
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS |
| **Database** | PostgreSQL 16 |
| **AI** | Mock provider (deterministic, default) / OpenAI provider (optional) |
| **Storage** | Local filesystem (development) / MinIO S3-compatible (production) |
| **Queue** | Redis + RQ (background workers) |
| **Infrastructure** | Docker Compose (local) / Railway + Vercel (cloud) |

---

## 4. Data Model

| Entity | Description |
|--------|-------------|
| **Project** | Top-level container for an assurance program. Owns all child entities. |
| **Requirement** | Extracted from source documents. Has criticality (low/medium/high/critical/catastrophic), human review status, and category. |
| **TestCase** | Imported test case record. Has type (unit/integration/system/safety/security/simulation) and expected outcome. |
| **Evidence** | Artifact record (test results, logs, documents). Has SHA-256 content hash, source, and collection date. |
| **TestRun** | Execution record for a TestCase. Has status (passed/failed/skipped/error) and timestamp. |
| **TraceLink** | Directed link from Requirement to TestCase or Requirement to Evidence. Has human review status (pending/approved/rejected) and AI confidence score. |
| **Gap** | Detected assurance gap for a Requirement. Has type (7 rule types), severity (low/medium/high/critical), and status (open/acknowledged/resolved). |
| **ReadinessScore** | Immutable snapshot of the weighted readiness calculation. Records component scores, caps applied, and overall score. |
| **MissionImpact** | Maps engineering gaps to operational consequences. Captures mission phase, impact category, and severity. |
| **ConfidenceScore** | AI confidence metadata for a TraceLink or extraction result. |
| **Standard** | Reference to a certification standard (DO-178C, STANAG, ISO 26262, etc.) against which requirements are mapped. |

---

## 5. Key Workflows

### (a) Requirement Extraction Workflow
1. User uploads requirements document (Markdown, PDF, DOCX) via the frontend or API.
2. Backend queues an AI extraction job (mock or OpenAI provider).
3. AI parses document and creates Requirement records with draft status.
4. User reviews AI-extracted requirements in the frontend — approves, edits, or rejects each.
5. Approved requirements become available for traceability linking.

### (b) Evidence Import Workflow
1. User uploads evidence artifact (JSON, CSV, document) or ATVP connector delivers a JSON export.
2. Backend computes SHA-256 content hash and stores the record.
3. Evidence is linked to a TestCase or TestRun via a TraceLink.
4. Evidence collection date is recorded for freshness evaluation in readiness scoring.

### (c) Gap Detection Workflow
1. User triggers `POST /api/v1/projects/{id}/gaps/detect`.
2. Gap service clears previous open gaps and re-evaluates from current project state.
3. Seven deterministic rules execute in sequence (see API Design for rule list).
4. Each detected gap creates a Gap record with type, severity, and linked requirement.
5. Results are returned immediately; user can acknowledge or resolve gaps.

### (d) Readiness Calculation Workflow
1. User triggers `POST /api/v1/projects/{id}/readiness/calculate`.
2. Readiness service loads all requirements, test cases, links, evidence, and gaps.
3. Six weighted component scores are computed (coverage 30%, pass rate 25%, evidence 20%, risk 10%, freshness 10%, human review 5%).
4. Up to six score caps are evaluated and the lowest applicable cap is applied.
5. An immutable ReadinessScore snapshot is created and returned with full explanation.

### (e) ATVP Integration Workflow
1. ATVP executes a scenario (e.g., GPS denial) and writes a structured JSON result file.
2. User imports the JSON via `POST /api/v1/projects/{id}/atvp/import` or the ATVP connector.
3. Backend creates TestRun and Evidence records from the ATVP export.
4. Evidence links to existing TestCases via scenario ID matching.
5. User re-runs gap detection and readiness calculation to reflect ATVP results.

---

## 6. API Design

- **Protocol**: RESTful HTTP/JSON
- **Authentication**: JWT Bearer tokens (HS256), issued at `/api/v1/auth/token`
- **Versioning**: All endpoints prefixed at `/api/v1`
- **Documentation**: OpenAPI 3.0 auto-generated at `/docs` (Swagger UI) and `/redoc`

| Resource Group | Base Path | Description |
|---------------|-----------|-------------|
| auth | `/api/v1/auth` | Login, token refresh |
| projects | `/api/v1/projects` | Project CRUD |
| documents | `/api/v1/projects/{id}/documents` | Document upload and management |
| requirements | `/api/v1/projects/{id}/requirements` | Requirement CRUD, extraction trigger |
| test-cases | `/api/v1/projects/{id}/test-cases` | Test case CRUD and import |
| evidence | `/api/v1/projects/{id}/evidence` | Evidence upload and management |
| trace-links | `/api/v1/projects/{id}/trace-links` | Link creation, approval, rejection |
| gaps | `/api/v1/projects/{id}/gaps` | Gap detection trigger, gap management |
| readiness | `/api/v1/projects/{id}/readiness` | Readiness calculation and history |
| reports | `/api/v1/projects/{id}/reports` | Report generation and download |
| mission-impact | `/api/v1/projects/{id}/mission-impact` | Mission impact analysis |
| confidence | `/api/v1/projects/{id}/confidence` | AI confidence scores |
| atvp | `/api/v1/projects/{id}/atvp` | ATVP scenario import |
| standards | `/api/v1/standards` | Certification standard reference data |

---

## 7. Security

| Control | Implementation |
|---------|---------------|
| **Authentication** | JWT HS256 tokens, configurable expiry |
| **Password storage** | bcrypt hashing, no plaintext storage |
| **Role-based access** | Three roles: `admin`, `engineer`, `viewer` |
| **Evidence integrity** | SHA-256 content hash on every evidence record |
| **Transport** | HTTPS enforced in production (Railway/Vercel TLS) |
| **CORS** | Configurable allowlist via `CORS_ORIGINS` environment variable |
| **Secrets** | All credentials via environment variables, never in source code |

---

## 8. Deployment

| Component | Platform | URL Pattern |
|-----------|----------|-------------|
| **Backend API** | Railway | `api.yourdomain.com` |
| **Frontend** | Vercel | `app.yourdomain.com` / `www.yourdomain.com` |
| **Database** | Railway PostgreSQL | Internal connection string |

Database migrations run automatically on startup (`alembic upgrade head`). Storage defaults to local filesystem in demo mode and switches to MinIO S3-compatible object storage in production by setting `OBJECT_STORAGE_PROVIDER=minio`.

See `docs/deployment/DEPLOYMENT_GUIDE.md` for step-by-step deployment instructions.
