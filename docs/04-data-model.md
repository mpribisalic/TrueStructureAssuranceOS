# Data Model

All primary keys are UUIDs. All models have `created_at` and (where applicable) `updated_at` timestamps.

---

## Organization
Tenant-level grouping. All projects and users belong to an organization.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| name | str | Organization name |
| industry | str | Primary industry |
| created_at | datetime | |
| updated_at | datetime | |

---

## User
System user belonging to an organization.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| organization_id | UUID | FK → Organization |
| email | str | Unique |
| name | str | Display name |
| password_hash | str | bcrypt hash |
| role | enum | admin / engineer / viewer |
| is_active | bool | Soft disable |
| created_at | datetime | |
| updated_at | datetime | |

---

## Project
An assurance project for one system or product.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| organization_id | UUID | FK → Organization |
| name | str | |
| description | str | Optional |
| industry | enum | defense/aerospace/medical/railway/industrial/automotive/space/robotics/energy/other |
| system_type | str | Free text — e.g. "autonomous_sensor" |
| criticality_level | enum | low/medium/high/mission_critical/safety_critical |
| status | enum | active / archived |
| created_at | datetime | |
| updated_at | datetime | |

---

## Document
An uploaded engineering artifact.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| uploaded_by_user_id | UUID | FK → User |
| filename | str | Original filename |
| file_type | str | txt/md/csv/json/pdf/docx |
| source_type | enum | requirements/user_stories/test_plan/test_cases/test_results/evidence/risk_assessment/standard/log/telemetry/report/other |
| storage_uri | str | MinIO object key |
| file_hash | str | SHA-256 of file content |
| file_size_bytes | int | |
| processing_status | enum | pending/processing/done/failed |
| extracted_text | text | Extracted plain text |
| processing_error | str | Error message if failed |
| created_at | datetime | |
| updated_at | datetime | |

---

## Requirement
A structured requirement extracted from a document or created manually.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| source_document_id | UUID | FK → Document, nullable |
| external_id | str | e.g. REQ-001 |
| title | str | Short title |
| text | text | Full requirement text |
| category | str | safety/security/functional/performance/interface/other |
| criticality | enum | low/medium/high/critical/catastrophic |
| priority | enum | low/medium/high |
| verification_method | str | test/analysis/inspection/demonstration |
| status | enum | draft/active/deprecated |
| ai_confidence | float | 0.0–1.0, null if manually created |
| source_reference | str | e.g. "requirements.md line 4" |
| human_review_status | enum | pending/approved/rejected |
| created_at | datetime | |
| updated_at | datetime | |

---

## TestCase
A test case imported from CSV or created manually.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| source_document_id | UUID | FK → Document, nullable |
| external_id | str | e.g. T-001 |
| title | str | |
| description | str | |
| test_type | str | system/unit/integration/simulation/inspection/analysis |
| automation_level | str | automated/manual/semi-automated |
| status | enum | active/deprecated |
| created_at | datetime | |
| updated_at | datetime | |

---

## TestRun
An execution of a test case, created during evidence import.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| test_case_id | UUID | FK → TestCase |
| external_id | str | Optional external reference |
| status | enum | passed/failed/blocked/skipped |
| executed_at | datetime | When the test was run |
| duration_seconds | float | Optional |
| environment | str | e.g. simulation/hardware-in-the-loop |
| result_summary | str | Human-readable summary |
| raw_result_uri | str | Link to raw output in storage, optional |
| created_at | datetime | |

---

## Evidence
A piece of evidence supporting a test run.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| source_document_id | UUID | FK → Document, nullable |
| test_run_id | UUID | FK → TestRun, nullable |
| title | str | |
| description | str | |
| evidence_type | str | test_result/log/simulation_output/screenshot/certificate/other |
| storage_uri | str | Optional file reference |
| hash | str | Optional content hash |
| created_by_user_id | UUID | FK → User |
| evidence_date | datetime | When the evidence was produced |
| created_at | datetime | |
| updated_at | datetime | |

---

## TraceLink
A link between a requirement and a test case (or evidence), created by AI suggestion or manually.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| source_type | str | requirement |
| source_id | UUID | FK → Requirement |
| target_type | str | test_case/evidence |
| target_id | UUID | FK → TestCase or Evidence |
| link_type | str | verifies/validates/demonstrates/supports |
| confidence | float | 0.0–1.0, null if manual |
| reason | str | AI explanation for the link |
| created_by | str | ai/user |
| human_review_status | enum | pending/approved/rejected |
| created_at | datetime | |
| updated_at | datetime | |

---

## Risk
An identified risk within a project.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| title | str | |
| description | str | |
| severity | enum | low/medium/high/critical/catastrophic |
| likelihood | enum | rare/unlikely/possible/likely/almost_certain |
| risk_level | enum | low/medium/high/critical — computed from severity × likelihood |
| mitigation_status | enum | open/in_progress/mitigated/accepted |
| related_requirement_id | UUID | FK → Requirement, nullable |
| created_at | datetime | |
| updated_at | datetime | |

---

## Gap
A detected coverage gap — output of deterministic gap detection.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| gap_type | enum | missing_test/missing_evidence/failed_test/missing_security_validation/missing_safety_validation/stale_evidence/unapproved_ai_suggestion |
| title | str | Short description |
| description | str | Full explanation |
| severity | enum | low/medium/high/critical |
| status | enum | open/acknowledged/resolved |
| related_requirement_id | UUID | FK → Requirement, nullable |
| related_test_case_id | UUID | FK → TestCase, nullable |
| related_evidence_id | UUID | FK → Evidence, nullable |
| ai_confidence | float | If AI contributed to detection |
| recommendation | str | Suggested action to resolve |
| created_at | datetime | |
| updated_at | datetime | |

---

## ReadinessScore
The output of one readiness calculation run.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| overall_score | float | 0–100 |
| coverage_score | float | % requirements with approved test link |
| test_pass_score | float | % linked test runs passing |
| evidence_score | float | % requirements with evidence |
| risk_score | float | % risks mitigated |
| freshness_score | float | % evidence within staleness threshold |
| human_review_score | float | % AI suggestions reviewed by humans |
| critical_blocker_count | int | Number of critical/catastrophic gaps |
| high_gap_count | int | |
| medium_gap_count | int | |
| low_gap_count | int | |
| explanation | text | Natural language explanation of score |
| caps_applied_json | JSON | List of score caps that triggered |
| top_blockers_json | JSON | Top 5 blocking gaps |
| recommended_actions_json | JSON | Top recommended actions |
| created_at | datetime | |

---

## Report
A generated readiness report.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project |
| readiness_score_id | UUID | FK → ReadinessScore |
| title | str | |
| report_type | str | readiness/gap_summary/audit |
| format | str | markdown |
| storage_uri | str | MinIO key for file version |
| content_markdown | text | Full Markdown content |
| created_by_user_id | UUID | FK → User |
| created_at | datetime | |

---

## AuditEvent
An immutable log entry for an important system action.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | PK |
| project_id | UUID | FK → Project, nullable |
| actor_user_id | UUID | FK → User |
| action | str | e.g. requirement.approved, trace_link.rejected |
| entity_type | str | requirement/test_case/trace_link/gap/report/etc |
| entity_id | UUID | ID of the affected entity |
| before_json | JSON | State before action, nullable |
| after_json | JSON | State after action, nullable |
| metadata_json | JSON | Additional context |
| created_at | datetime | Immutable timestamp |
