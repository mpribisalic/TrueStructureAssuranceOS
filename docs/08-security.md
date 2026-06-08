# Security Design

## Authentication

All API endpoints (except `/health` and `/api/v1/auth/login`) require a valid JWT token.

- Tokens are issued on login with a configurable expiry (`JWT_EXPIRES_MINUTES`, default 1440 = 24h)
- Tokens are signed with `JWT_SECRET` — must be a strong random string in production
- Token validation uses `python-jose` with HS256 algorithm

## Authorization

Three roles with increasing permissions:

| Role | Can do |
|------|--------|
| viewer | Read projects, requirements, test cases, evidence, reports, gaps, scores |
| engineer | Everything viewer can + upload documents, approve/reject AI suggestions, create manual items |
| admin | Everything engineer can + create/delete projects, manage users |

## File Upload Security

All uploaded files are validated before processing:

1. File extension checked against allowed list (txt, md, csv, json, pdf, docx)
2. File size checked against `MAX_UPLOAD_SIZE_MB` limit (default 25 MB)
3. SHA-256 hash computed before storage
4. Files stored in MinIO with non-guessable object keys (UUID-based)
5. Files are never executed — only text is extracted

## AI Prompt Injection Prevention

Uploaded documents are untrusted external input. A malicious actor could embed instructions in a requirements document to manipulate the AI.

Mitigations:

1. System prompt explicitly instructs the model that document content is untrusted
2. System prompt forbids the model from following instructions embedded in documents
3. AI output is validated against strict Pydantic schemas — unexpected fields are rejected
4. AI output is marked as `pending_review` — human must approve before it affects scores
5. Audit log records all AI calls and outputs

## Secrets Management

- All secrets are environment variables — never hardcoded
- `.env` file is in `.gitignore` — only `.env.example` is committed
- In production: use a secrets manager (AWS Secrets Manager, Vault, etc.)
- JWT_SECRET must be regenerated per environment

## Audit Trail

All important actions are recorded as AuditEvent records:

- User login
- Requirement approved / rejected
- Trace link approved / rejected
- Gap detection run
- Readiness score calculated
- Report generated
- Document uploaded
- User created / deactivated

AuditEvents are immutable — they are never updated or deleted.

## Future Security Considerations

These are not implemented in TRL 4 but are designed for:

### On-premises deployment
The architecture supports deployment without cloud dependencies:
- MinIO replaces S3
- PostgreSQL runs locally
- No calls to external APIs (with mock AI provider)

### Air-gapped deployment
With mock AI provider and local infrastructure, the entire system can run without internet access. This is validated by the mock provider design.

### Network segmentation
In production, the API should not be directly internet-facing. Place behind a reverse proxy (nginx, Caddy) with TLS termination.

### Data classification
No classified data handling is implemented. For classified environments, additional controls (encryption at rest, access logging, network isolation) are required and outside the scope of TRL 4.
