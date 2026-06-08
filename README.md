# True Structure Mission Assurance Platform

> AI-assisted certification readiness and mission assurance intelligence for defense and safety-critical systems.

**True Structure** transforms unstructured engineering artifacts — requirements documents, test case specifications, and evidence records — into traceable, explainable readiness scores, gap analyses, and certification reports. Designed for dual-use across defense autonomous systems validation and civil regulated industries (DO-178C, ISO 26262, IEC 62304).

---

## Architecture

The platform comprises two integrated components:

- **Assurance OS** — FastAPI backend + Next.js frontend. Manages the full requirements → test → evidence → gap → readiness → report chain. 12 build phases complete.
- **ATVP (Autonomous Test Validation Platform)** — ArduPilot SITL-based simulation environment for autonomous system test execution. Exports structured JSON evidence files consumed by the Assurance OS.

```
Requirement → Test Case → Evidence → Gap Detection → Readiness Score → Report
```

See [`docs/diana/ARCHITECTURE.md`](docs/diana/ARCHITECTURE.md) for the full architecture document.

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- `make`

### Run locally

```bash
cp .env.example .env
make up
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

### Load the demo dataset

```bash
make seed-demo
```

This loads the Autonomous Reconnaissance Sensor Platform (ARSP) sample dataset — 8 requirements, 5 test cases, 5 evidence records, with intentional gaps for demonstration.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2, Alembic |
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Database | PostgreSQL 16 |
| Queue | Redis + RQ |
| Storage | Local filesystem (dev) / MinIO S3 (production) |
| AI | Mock provider (deterministic, default) / OpenAI (optional) |
| Infrastructure | Docker Compose / Railway / Vercel |

---

## Make Commands

| Command | Description |
|---------|-------------|
| `make up` | Start all services |
| `make down` | Stop all services |
| `make reset` | Reset and restart (clears volumes) |
| `make logs` | Follow logs |
| `make migrate` | Run database migrations |
| `make seed-demo` | Load defense-autonomy demo dataset |
| `make backend-test` | Run backend tests |
| `make frontend-test` | Run frontend tests |
| `make lint` | Lint all code |
| `make format` | Format backend code |

---

## Test Results

```
97/97 tests passing
```

Run: `make backend-test`  
Suite: `apps/api/tests/test_golden_demo.py` — full end-to-end coverage from user creation to report download.

---

## Build Phases Completed

| Phase | Description |
|-------|-------------|
| 13 | Core data models and database schema |
| 14 | Requirement extraction service with AI provider abstraction |
| 15 | Test case import and management |
| 16 | Evidence import with SHA-256 integrity |
| 17 | Traceability link management with human review gates |
| 18 | Deterministic gap detection (7 rules) |
| 19 | Weighted readiness scoring engine (6 caps) |
| 20 | DIANA documentation — architecture, TRL assessment, validation plan, dual-use positioning |

---

## Documentation

### DIANA Documentation (NATO)

| Document | Description |
|----------|-------------|
| [`docs/diana/ARCHITECTURE.md`](docs/diana/ARCHITECTURE.md) | Platform architecture, technology stack, data model, key workflows, API design |
| [`docs/diana/TRL_ASSESSMENT.md`](docs/diana/TRL_ASSESSMENT.md) | TRL 4 assessment for ATVP and Assurance OS components |
| [`docs/diana/VALIDATION_PLAN.md`](docs/diana/VALIDATION_PLAN.md) | Five validation scenarios, demo dataset specification, automated test suite |
| [`docs/diana/DUAL_USE_POSITIONING.md`](docs/diana/DUAL_USE_POSITIONING.md) | Defense and civil applications, market analysis, NATO DIANA alignment, pilot strategy |

### Deployment

[`docs/deployment/DEPLOYMENT_GUIDE.md`](docs/deployment/DEPLOYMENT_GUIDE.md) — Railway (backend), Vercel (frontend), PostgreSQL deployment guide.

---

## Disclaimer

This platform is AI-assisted and does not represent formal regulatory certification or approval. All findings must be reviewed by qualified engineering, safety, compliance, or mission assurance personnel.
