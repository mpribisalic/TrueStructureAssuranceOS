// Auth
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Projects
export interface Project {
  id: string;
  name: string;
  description?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectPayload {
  name: string;
  description?: string;
}

// Requirements
export type RequirementStatus = "pending" | "approved" | "rejected";
export type RequirementCriticality = "critical" | "high" | "medium" | "low";

export interface Requirement {
  id: string;
  project_id: string;
  external_id: string;
  title: string;
  description?: string;
  category?: string;
  criticality: RequirementCriticality;
  status: RequirementStatus;
  source_document_id?: string;
  created_at: string;
  updated_at: string;
}

// Test Cases
export type TestStatus = "pending" | "passed" | "failed" | "skipped";
export type TestType = "unit" | "integration" | "system" | "acceptance" | string;

export interface TestCase {
  id: string;
  project_id: string;
  external_id: string;
  title: string;
  description?: string;
  test_type: TestType;
  status: TestStatus;
  created_at: string;
  updated_at: string;
}

// Evidence
export interface Evidence {
  id: string;
  project_id: string;
  title: string;
  description?: string;
  source: string;
  evidence_type?: string;
  created_at: string;
  updated_at: string;
}

// Trace Links
export type TraceLinkStatus = "pending" | "approved" | "rejected";

export interface TraceLink {
  id: string;
  project_id: string;
  requirement_id: string;
  test_case_id: string;
  status: TraceLinkStatus;
  confidence_score?: number;
  requirement?: Requirement;
  test_case?: TestCase;
  created_at: string;
  updated_at: string;
}

// Gaps
export type GapSeverity = "critical" | "high" | "medium" | "low";
export type GapStatus = "open" | "resolved" | "accepted";
export type GapType = "missing_test" | "missing_evidence" | "untested_requirement" | string;

export interface Gap {
  id: string;
  project_id: string;
  gap_type: GapType;
  title: string;
  description?: string;
  severity: GapSeverity;
  status: GapStatus;
  requirement_id?: string;
  created_at: string;
  updated_at: string;
}

// Readiness
export interface ReadinessScore {
  id: string;
  project_id: string;
  overall_score: number;
  coverage_score: number;
  test_pass_score: number;
  evidence_score: number;
  risk_score: number;
  freshness_score: number;
  human_review_score: number;
  caps_applied: string[];
  calculated_at: string;
}

// Reports
export interface Report {
  id: string;
  project_id: string;
  title: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface CreateReportPayload {
  title: string;
}

// Document
export interface Document {
  id: string;
  project_id: string;
  filename: string;
  content_type: string;
  created_at: string;
}
