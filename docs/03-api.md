# API Reference

Base URL: `http://localhost:8000`

All protected endpoints require: `Authorization: Bearer <token>`

Interactive docs: `http://localhost:8000/docs`

---

## Health

### GET /health
Returns service health status. No authentication required.

**Response**
```json
{
  "status": "ok",
  "app": "True Structure Assurance OS",
  "env": "local"
}
```

---

## Auth

### POST /api/v1/auth/login
Authenticate and receive JWT token.

**Body**
```json
{ "email": "demo@example.com", "password": "demo1234" }
```

**Response**
```json
{ "access_token": "...", "token_type": "bearer" }
```

### GET /api/v1/auth/me
Returns current authenticated user.

### POST /api/v1/auth/logout
Invalidates current session.

---

## Projects

### GET /api/v1/projects
List all projects for the current organization.

### POST /api/v1/projects
Create a new project.

**Body**
```json
{
  "name": "Autonomous Reconnaissance Sensor Platform",
  "description": "...",
  "industry": "defense",
  "system_type": "autonomous_sensor",
  "criticality_level": "mission_critical"
}
```

### GET /api/v1/projects/{project_id}
Get project details.

### PATCH /api/v1/projects/{project_id}
Update project fields.

### DELETE /api/v1/projects/{project_id}
Delete project (admin only).

---

## Documents

### POST /api/v1/projects/{project_id}/documents
Upload a document file. Multipart form.

**Form fields**
- `file` — the file
- `source_type` — requirements | user_stories | test_cases | test_results | evidence | risk_assessment | standard | other

### GET /api/v1/projects/{project_id}/documents
List documents for a project.

### GET /api/v1/documents/{document_id}
Get document details and extracted text.

### POST /api/v1/documents/{document_id}/process
Trigger text extraction (if not done automatically).

---

## Requirements

### POST /api/v1/documents/{document_id}/extract-requirements
Run AI extraction on a document. Returns extracted requirements for review.

### GET /api/v1/projects/{project_id}/requirements
List requirements. Supports filters: `?status=active&category=safety`

### POST /api/v1/projects/{project_id}/requirements
Create a requirement manually.

### PATCH /api/v1/requirements/{requirement_id}
Update requirement fields.

### POST /api/v1/requirements/{requirement_id}/approve
Approve an AI-suggested requirement (sets human_review_status=approved).

### POST /api/v1/requirements/{requirement_id}/reject
Reject an AI-suggested requirement.

---

## Test Cases

### POST /api/v1/projects/{project_id}/test-cases/import
Import test cases from CSV.

**CSV format**
```csv
external_id,title,description,test_type,automation_level,status
T-001,Baseline test,...,system,automated,active
```

### GET /api/v1/projects/{project_id}/test-cases
List test cases.

### GET /api/v1/test-cases/{test_case_id}
Get test case details.

---

## Evidence

### POST /api/v1/projects/{project_id}/evidence/import
Import evidence from JSON. Creates TestRun + Evidence records.

**JSON format**
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

### GET /api/v1/projects/{project_id}/evidence
List evidence.

### GET /api/v1/evidence/{evidence_id}
Get evidence details.

---

## Traceability

### POST /api/v1/projects/{project_id}/trace-links/suggest
Run AI trace suggestion. Creates pending TraceLink records.

### GET /api/v1/projects/{project_id}/trace-links
List trace links. Supports filter: `?status=pending`

### POST /api/v1/trace-links/{trace_link_id}/approve
Approve a trace link.

### POST /api/v1/trace-links/{trace_link_id}/reject
Reject a trace link.

---

## Gaps

### POST /api/v1/projects/{project_id}/gaps/detect
Run deterministic gap detection. Replaces existing gaps for this run.

### GET /api/v1/projects/{project_id}/gaps
List gaps. Supports filter: `?severity=critical`

### PATCH /api/v1/gaps/{gap_id}
Update gap status or add notes.

---

## Readiness

### POST /api/v1/projects/{project_id}/readiness/calculate
Calculate readiness score. Returns full score with explanation.

### GET /api/v1/projects/{project_id}/readiness/latest
Get the latest readiness score.

### GET /api/v1/projects/{project_id}/readiness/history
Get score history (list of ReadinessScore records).

---

## Reports

### POST /api/v1/projects/{project_id}/reports
Generate a new readiness report. Uses the latest readiness score.

**Body**
```json
{ "title": "ARSP Readiness Report — June 2026", "report_type": "readiness" }
```

### GET /api/v1/projects/{project_id}/reports
List reports.

### GET /api/v1/reports/{report_id}
Get report content (Markdown).

---

## Error Responses

| Code | Meaning |
|------|---------|
| 400 | Validation error — check request body |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient role permissions |
| 404 | Resource not found |
| 422 | Unprocessable entity — Pydantic validation failed |
| 500 | Internal server error |

All errors return:
```json
{ "detail": "Human-readable error message" }
```
