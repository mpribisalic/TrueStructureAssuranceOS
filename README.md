# True Structure Assurance OS

> AI Certification Readiness Platform for Defense, Dual-Use and Regulated Safety-Critical Systems

**True Structure Assurance OS** turns unstructured engineering artifacts into explainable certification and mission readiness intelligence.

---

## Quick Start

```bash
cp .env.example .env
make up
```

- API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2, Alembic |
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Database | PostgreSQL 16 |
| Queue | Redis + RQ |
| Storage | MinIO (S3-compatible) |
| AI | Mock (default) / OpenAI (optional) |
| Infrastructure | Docker Compose |

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

## Core Workflow

```
Requirement → Test → Evidence → Gap → Readiness Score → Report
```

1. Upload engineering artifacts (requirements, test cases, evidence)
2. AI extracts and structures requirements (human review required)
3. AI suggests traceability links (human approval required)
4. Deterministic gap detection identifies missing coverage
5. Readiness score calculated with caps and explanations
6. Explainable report generated for evaluators/auditors

---

## Demo Dataset

Located in `samples/defense-autonomy/` — simulates an Autonomous Reconnaissance Sensor Platform with 8 requirements, 5 test cases, and intentional gaps.

```bash
make seed-demo
```

---

## TRL 4 Evidence Package

See `docs/trl4-evidence/` for NATO DIANA TRL 4 validation documentation.

---

## Disclaimer

This platform is AI-assisted and does not represent formal regulatory certification or approval.
All findings must be reviewed by qualified engineering, safety, compliance or mission assurance personnel.
