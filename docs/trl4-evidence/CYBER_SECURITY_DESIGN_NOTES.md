# Cybersecurity Design Notes

**Product:** True Structure Assurance OS TRL 4 Prototype
**Date:** 2026-06-08

---

## Authentication

- JWT (JSON Web Tokens) using HS256 algorithm
- `python-jose` library for token signing and validation
- Configurable token expiry via `JWT_EXPIRES_MINUTES` (default: 1440 minutes = 24 hours)
- `JWT_SECRET` must be set as an environment variable — never hardcoded
- All API endpoints except `/health` and `/auth/login` require a valid JWT

## Authorization

Three roles with least-privilege design:

| Role | Scope |
|------|-------|
| viewer | Read-only access to all project data and reports |
| engineer | viewer + create/edit, document upload, AI suggestion review |
| admin | engineer + project delete, user management |

Role is enforced at the route level via FastAPI dependency injection.

## File Upload Security

1. File extension validated against allowlist: `{txt, md, csv, json, pdf, docx}`
2. File size validated against `MAX_UPLOAD_SIZE_MB` (default 25 MB)
3. SHA-256 hash computed before storage (enables duplicate detection and integrity verification)
4. Files stored with UUID-based object keys — not guessable
5. Files are never executed — text is extracted using library parsers only
6. File MIME type is not trusted — extension check is the primary control

## AI Prompt Injection Prevention

Uploaded documents are untrusted external input. An adversary could embed LLM instructions in a requirements document to manipulate AI output.

Controls:

1. System prompt explicitly declares document content as untrusted
2. System prompt forbids the model from following instructions in document content
3. All AI responses are validated against strict Pydantic schemas — extra fields rejected
4. AI output is always `pending_review` — human must approve before it affects any score
5. The deterministic scoring engine does not call any AI — it cannot be influenced by injected content
6. Audit log records all AI calls, inputs and outputs

## Secrets Management

- All secrets are environment variables only
- `.env` file is in `.gitignore` and never committed
- `.env.example` contains only placeholder values (no real secrets)
- Production deployment must use a secrets manager or environment injection
- `JWT_SECRET` must be freshly generated per environment: `openssl rand -hex 32`

## Audit Trail

All important actions are recorded as immutable `AuditEvent` records:

- User login / logout
- Document uploaded
- Requirement approved / rejected
- Trace link approved / rejected
- Gap detection run
- Readiness score calculated
- Report generated
- User created / deactivated

AuditEvent records are insert-only — never updated or deleted.

## Future: On-Premises Deployment

The architecture is designed to support on-premises deployment:

- No cloud dependencies required (mock AI, local MinIO, local PostgreSQL)
- Docker Compose supports air-gapped environments
- All dependencies are open-source with known licenses
- No telemetry or usage reporting

## Future: Air-Gapped Deployment

With `LLM_PROVIDER=mock`, the system makes zero external network calls. Suitable for air-gapped environments after initial Docker image pull. For fully air-gapped operation, images must be pre-loaded via a private registry.

## Known Gaps (TRL 4)

- No TLS — production deployment requires reverse proxy with TLS termination
- No penetration testing performed
- No formal security audit
- No rate limiting on API endpoints
- Password hashing uses bcrypt — adequate for TRL 4, FIPS compliance not verified
