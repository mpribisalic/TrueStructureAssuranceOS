# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser / Client                      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
┌──────────────────────────▼──────────────────────────────────┐
│                    Next.js Frontend (port 3000)              │
│  React + TypeScript + Tailwind CSS + TanStack Query + Zod   │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API calls
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend (port 8000)               │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Routes  │→ │ Services │→ │  Repos   │→ │   DB     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                      │                                       │
│               ┌──────▼──────┐                               │
│               │ AI Provider │ (mock / OpenAI)               │
│               └─────────────┘                               │
│                      │                                       │
│               ┌──────▼──────┐                               │
│               │  RQ Worker  │ (background jobs)             │
│               └─────────────┘                               │
└──────────────────────────────────────────────────────────────┘
         │                  │                  │
┌────────▼───────┐  ┌───────▼──────┐  ┌───────▼──────┐
│  PostgreSQL 16 │  │   Redis 7    │  │   MinIO      │
│  (primary DB)  │  │  (job queue) │  │  (file store)│
└────────────────┘  └──────────────┘  └──────────────┘
```

## Backend Layer Design

### Routes (`app/api/v1/`)
- Receive HTTP requests, validate with Pydantic schemas
- Call service layer only — no business logic here
- Return Pydantic response schemas

### Services (`app/services/`)
- Contain all business logic
- Orchestrate multiple repositories and AI calls
- Create audit events for important actions
- Never access the database directly — use repositories

### Repositories (`app/repositories/`)
- All database access via SQLAlchemy
- Return domain model objects
- No business logic

### AI Layer (`app/ai/`)
- `AIProvider` abstract interface
- `MockAIProvider` — deterministic, no network calls, used for tests and demo
- `OpenAIProvider` — optional, requires `OPENAI_API_KEY`
- Provider selected by `LLM_PROVIDER` env var

### Scoring (`app/scoring/`)
- Pure deterministic functions — no AI, no randomness
- `GapDetector` — applies 7 deterministic gap rules
- `ReadinessCalculator` — weighted formula with score caps

### Documents (`app/documents/`)
- File validation, hash calculation, text extraction
- Supports: txt, md, csv, json, pdf, docx
- Storage abstraction over MinIO/S3

## Data Flow: Document → Readiness Report

```
1. User uploads file
   → File validated (type, size, hash)
   → Stored in MinIO
   → Document record created (status: pending)

2. User triggers extraction
   → Text extracted from file
   → AI provider called: extract_requirements(text)
   → Requirements created (status: pending_review)

3. User reviews AI suggestions
   → Approve/reject each requirement
   → Approved requirements become active

4. User imports test cases (CSV) and evidence (JSON)
   → TestCase records created
   → TestRun + Evidence records created

5. User triggers trace suggestion
   → AI provider called: suggest_trace_links(requirements, test_cases)
   → TraceLink records created (status: pending_review)

6. User approves/rejects trace links
   → Approved links become active

7. User triggers gap detection
   → GapDetector runs 7 deterministic rules
   → Gap records created

8. User triggers readiness calculation
   → ReadinessCalculator runs weighted formula
   → Score caps applied
   → ReadinessScore record created

9. User generates report
   → Markdown report assembled from all data
   → Report stored in MinIO
   → Report record created
```

## Database Schema Overview

See `docs/04-data-model.md` for full schema.

Core entities and relationships:

```
Organization
  └── User (many)
  └── Project (many)
       ├── Document (many)
       ├── Requirement (many)  ←── Document
       ├── TestCase (many)     ←── Document
       ├── TestRun (many)      ←── TestCase
       ├── Evidence (many)     ←── TestRun, Document
       ├── TraceLink (many)    ←── Requirement, TestCase
       ├── Risk (many)
       ├── Gap (many)
       ├── ReadinessScore (many)
       ├── Report (many)
       └── AuditEvent (many)
```

## Security Architecture

See `docs/08-security.md` and `docs/trl4-evidence/CYBER_SECURITY_DESIGN_NOTES.md`.

- JWT authentication on all protected endpoints
- Role-based access: admin, engineer, viewer
- File validation before storage
- AI prompt injection prevention (documents treated as untrusted data)
- All secrets via environment variables
- Audit trail for all important actions

## Deployment

See `docs/10-deployment.md`.

Local development: `make up` starts all 6 Docker services.
