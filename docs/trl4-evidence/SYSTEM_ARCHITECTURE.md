# System Architecture — TRL 4 Evidence

**Product:** True Structure Assurance OS
**Version:** 0.1.0
**Date:** 2026-06-08

---

## Architecture Summary

True Structure Assurance OS is a web application with a React frontend, FastAPI backend, PostgreSQL database, Redis job queue, and MinIO object storage. All components run in Docker containers orchestrated by Docker Compose.

The core design separates AI-assisted functions (extraction, suggestion) from deterministic functions (gap detection, scoring) to ensure auditability and reproducibility.

---

## Component Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend API | FastAPI | 0.115+ |
| Backend language | Python | 3.12 |
| ORM | SQLAlchemy | 2.x |
| Schema validation | Pydantic | v2 |
| Database migrations | Alembic | 1.13+ |
| Database | PostgreSQL | 16 |
| Job queue | Redis + RQ | 7 / 1.16 |
| Object storage | MinIO (S3-compatible) | latest |
| Frontend framework | Next.js | 15 |
| Frontend language | TypeScript | 5 |
| UI components | Tailwind CSS + shadcn/ui | 3.4 |
| Data fetching | TanStack Query | 5 |
| Validation | Zod | 3.23 |
| Charts | Recharts | 2.12 |
| Containerization | Docker + Compose | 24+ / v2 |
| Linting | ruff | 0.4+ |
| Testing | pytest | 8+ |

---

## Layer Separation

```
HTTP Request
    ↓
FastAPI Router (apps/api/app/api/v1/)
    → Input validation (Pydantic schemas)
    ↓
Service Layer (apps/api/app/services/)
    → Business logic
    → Orchestrates repositories and AI
    → Creates audit events
    ↓
Repository Layer (apps/api/app/repositories/)
    → Database access only (SQLAlchemy)
    ↓
Database (PostgreSQL)

AI Layer (apps/api/app/ai/)
    → Called by services only
    → Replaceable provider interface
    → Mock and OpenAI implementations

Scoring Layer (apps/api/app/scoring/)
    → Pure deterministic functions
    → No AI, no database access
    → Called by services
```

---

## AI Provider Abstraction

The `AIProvider` abstract class defines the interface. The active provider is selected at startup via the `LLM_PROVIDER` environment variable:

- `mock` — deterministic, no network, default
- `openai` — requires `OPENAI_API_KEY`, uses gpt-4.1-mini by default

This design allows future providers (local LLM, Azure OpenAI, Anthropic) to be added without changing service logic.

---

## Data Flow Diagram

```
Upload                 Extract              Review
PDF/Word/CSV/JSON  →   Text extraction  →   AI suggestion
        ↓                    ↓                   ↓
  Document record      Requirement/          pending_review
  (MinIO + DB)         TestCase records      ↓
                                         approve/reject
                                             ↓
                                         active record

active requirements + test cases + evidence
        ↓
  AI trace suggestion → pending links → approve/reject → active links
        ↓
  Gap detection (deterministic, 7 rules) → Gap records
        ↓
  Readiness scoring (deterministic, formula + caps) → ReadinessScore
        ↓
  Report generation → Markdown report → storage + DB record
```

---

## Deployment Architecture

```
Docker Compose (local/production)
├── api         (port 8000)   FastAPI, uvicorn
├── worker      (no port)     RQ worker for background jobs
├── web         (port 3000)   Next.js, node server
├── postgres    (port 5432)   PostgreSQL 16
├── redis       (port 6379)   Redis 7
└── minio       (port 9000)   MinIO object storage
               (port 9001)   MinIO console
```

All services communicate over a private Docker network. Only `api`, `web`, and `minio` (console) ports are exposed to the host.
