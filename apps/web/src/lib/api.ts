import { getToken } from "./auth";
import type {
  LoginResponse,
  Project,
  CreateProjectPayload,
  Requirement,
  TestCase,
  Evidence,
  TraceLink,
  Gap,
  ReadinessScore,
  Report,
  CreateReportPayload,
  Document,
} from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const API_BASE = `${BASE_URL}/api/v1`;

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => res.statusText);
    throw new Error(errorText || `HTTP ${res.status}`);
  }

  const contentType = res.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    return res.json() as Promise<T>;
  }
  return res.blob() as unknown as Promise<T>;
}

// Auth
export async function login(username: string, password: string): Promise<LoginResponse> {
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
  });
  if (!res.ok) {
    const errorText = await res.text().catch(() => res.statusText);
    throw new Error(errorText || `HTTP ${res.status}`);
  }
  return res.json();
}

// Projects
export const getProjects = (): Promise<Project[]> =>
  request<Project[]>("/projects");

export const getProject = (id: string): Promise<Project> =>
  request<Project>(`/projects/${id}`);

export const createProject = (data: CreateProjectPayload): Promise<Project> =>
  request<Project>("/projects", {
    method: "POST",
    body: JSON.stringify(data),
  });

// Requirements
export const getRequirements = (projectId: string): Promise<Requirement[]> =>
  request<Requirement[]>(`/projects/${projectId}/requirements`);

export const approveRequirement = (reqId: string): Promise<Requirement> =>
  request<Requirement>(`/requirements/${reqId}/approve`, { method: "POST" });

export const rejectRequirement = (reqId: string): Promise<Requirement> =>
  request<Requirement>(`/requirements/${reqId}/reject`, { method: "POST" });

export const uploadDocument = (projectId: string, file: File): Promise<Document> => {
  const form = new FormData();
  form.append("file", file);
  return request<Document>(`/projects/${projectId}/documents`, {
    method: "POST",
    body: form,
  });
};

export const extractRequirements = (documentId: string): Promise<Requirement[]> =>
  request<Requirement[]>(`/documents/${documentId}/extract-requirements`, {
    method: "POST",
  });

// Test Cases
export const getTestCases = (projectId: string): Promise<TestCase[]> =>
  request<TestCase[]>(`/projects/${projectId}/test-cases`);

export const importTestCases = (projectId: string, file: File): Promise<TestCase[]> => {
  const form = new FormData();
  form.append("file", file);
  return request<TestCase[]>(`/projects/${projectId}/test-cases/import`, {
    method: "POST",
    body: form,
  });
};

// Evidence
export const getEvidence = (projectId: string): Promise<Evidence[]> =>
  request<Evidence[]>(`/projects/${projectId}/evidence`);

export const importEvidence = (projectId: string, file: File): Promise<Evidence[]> => {
  const form = new FormData();
  form.append("file", file);
  return request<Evidence[]>(`/projects/${projectId}/evidence/import`, {
    method: "POST",
    body: form,
  });
};

// Trace Links
export const getTraceLinks = (projectId: string): Promise<TraceLink[]> =>
  request<TraceLink[]>(`/projects/${projectId}/trace-links`);

export const suggestTraceLinks = (projectId: string): Promise<TraceLink[]> =>
  request<TraceLink[]>(`/projects/${projectId}/trace-links/suggest`, {
    method: "POST",
  });

export const approveTraceLink = (linkId: string): Promise<TraceLink> =>
  request<TraceLink>(`/trace-links/${linkId}/approve`, { method: "POST" });

// Gaps
export const getGaps = (projectId: string): Promise<Gap[]> =>
  request<Gap[]>(`/projects/${projectId}/gaps`);

export const detectGaps = (projectId: string): Promise<Gap[]> =>
  request<Gap[]>(`/projects/${projectId}/gaps/detect`, { method: "POST" });

// Readiness
export const getReadiness = (projectId: string): Promise<ReadinessScore> =>
  request<ReadinessScore>(`/projects/${projectId}/readiness`);

export const calculateReadiness = (projectId: string): Promise<ReadinessScore> =>
  request<ReadinessScore>(`/projects/${projectId}/readiness/calculate`, {
    method: "POST",
  });

// Reports
export const getReports = (projectId: string): Promise<Report[]> =>
  request<Report[]>(`/projects/${projectId}/reports`);

export const createReport = (projectId: string, data: CreateReportPayload): Promise<Report> =>
  request<Report>(`/projects/${projectId}/reports`, {
    method: "POST",
    body: JSON.stringify(data),
  });

export const downloadReport = (reportId: string): Promise<Blob> =>
  request<Blob>(`/reports/${reportId}/download`);
