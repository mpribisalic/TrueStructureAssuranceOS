"""Deterministic mock AI provider — no network required.

Parses plain-text patterns (REQ-NNN:, ## REQ-NNN, numbered lines) to produce
structured requirements. Output is fully deterministic for a given input,
making it suitable for tests, offline mode, and the TRL 4 DIANA demo.
"""
import re

from app.ai.base import (
    AIProvider,
    ExtractedRequirement,
    GapExplanationResult,
    ReportSummaryResult,
    RequirementExtractionResult,
    SuggestedLink,
    TraceSuggestionResult,
)

# Matches patterns like: REQ-001: title text  or  ## REQ-001\ntext
_REQ_INLINE = re.compile(
    r"\b(REQ-\d+)\s*[:\-]\s*(.+)",
    re.IGNORECASE,
)
_REQ_HEADING = re.compile(
    r"^#{1,3}\s+(REQ-\d+)\s*\n+([\s\S]+?)(?=^#|\Z)",
    re.MULTILINE | re.IGNORECASE,
)

_CATEGORY_KEYWORDS = {
    "safety": ["safe", "hazard", "fault", "fail", "emergency", "protect"],
    "security": ["secur", "auth", "encrypt", "access control", "crypto", "unauthori"],
    "performance": ["latency", "throughput", "response time", "bandwidth", "speed", "ms"],
    "reliability": ["availab", "uptime", "mtbf", "recover", "redundan"],
    "functional": [],
}

_CRITICALITY_KEYWORDS = {
    "catastrophic": ["catastrophic", "shall not", "must not", "death", "life-critical"],
    "critical": ["critical", "shall maintain", "safety-critical", "mission-critical"],
    "high": ["high", "shall", "must"],
    "medium": ["should", "medium"],
    "low": ["may", "optional", "low"],
}


def _infer_category(text: str) -> str:
    lower = text.lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        if category == "functional":
            continue
        if any(kw in lower for kw in keywords):
            return category
    return "functional"


def _infer_criticality(text: str) -> str:
    lower = text.lower()
    for criticality, keywords in _CRITICALITY_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return criticality
    return "medium"


def _infer_verification(text: str) -> str:
    lower = text.lower()
    if any(kw in lower for kw in ["inspect", "review", "document"]):
        return "inspection"
    if any(kw in lower for kw in ["analy", "model", "simulat"]):
        return "analysis"
    if any(kw in lower for kw in ["demonstrat", "show"]):
        return "demonstration"
    return "test"


class MockAIProvider(AIProvider):
    """Deterministic, offline AI provider used for tests and the DIANA demo."""

    def extract_requirements(self, text: str) -> RequirementExtractionResult:
        seen: dict[str, ExtractedRequirement] = {}

        # Match heading-style: ## REQ-001\nfull text block
        for match in _REQ_HEADING.finditer(text):
            req_id = match.group(1).upper()
            body = match.group(2).strip()
            title = body.splitlines()[0][:200]
            if req_id not in seen:
                seen[req_id] = ExtractedRequirement(
                    external_id=req_id,
                    title=title,
                    text=body,
                    category=_infer_category(body),
                    criticality=_infer_criticality(body),
                    verification_method=_infer_verification(body),
                    confidence=0.88,
                    source_reference=f"heading {req_id}",
                )

        # Match inline: REQ-001: text on same line
        for i, line in enumerate(text.splitlines(), start=1):
            m = _REQ_INLINE.search(line)
            if m:
                req_id = m.group(1).upper()
                body = m.group(2).strip()
                if req_id not in seen:
                    seen[req_id] = ExtractedRequirement(
                        external_id=req_id,
                        title=body[:200],
                        text=body,
                        category=_infer_category(body),
                        criticality=_infer_criticality(body),
                        verification_method=_infer_verification(body),
                        confidence=0.82,
                        source_reference=f"line {i}",
                    )

        return RequirementExtractionResult(requirements=list(seen.values()))

    def suggest_trace_links(self, requirements, test_cases, evidence) -> TraceSuggestionResult:
        links: list[SuggestedLink] = []
        for req in requirements:
            for tc in test_cases:
                req_id = getattr(req, "external_id", "")
                tc_id = getattr(tc, "external_id", "")
                req_text = (getattr(req, "text", "") or "").lower()
                tc_text = (
                    (getattr(tc, "title", "") or "") + " " + (getattr(tc, "description", "") or "")
                ).lower()
                # Simple overlap heuristic — count shared words
                req_words = set(re.findall(r"\w{4,}", req_text))
                tc_words = set(re.findall(r"\w{4,}", tc_text))
                overlap = len(req_words & tc_words)
                if overlap >= 2:
                    confidence = min(0.5 + overlap * 0.05, 0.95)
                    links.append(
                        SuggestedLink(
                            requirement_external_id=req_id,
                            test_case_external_id=tc_id,
                            link_type="verifies",
                            confidence=round(confidence, 2),
                            reason=f"Shared keywords: {', '.join(list(req_words & tc_words)[:5])}",
                        )
                    )
        return TraceSuggestionResult(links=links)

    def explain_gaps(self, gaps) -> GapExplanationResult:
        count = len(gaps) if gaps else 0
        return GapExplanationResult(
            summary=f"The project has {count} validation gap(s) affecting certification readiness.",
            recommended_actions=[
                "Review all requirements without approved test coverage.",
                "Ensure evidence is linked to executed test cases.",
                "Address high-severity gaps before TRL assessment.",
            ],
        )

    def generate_report_summary(self, context) -> ReportSummaryResult:
        return ReportSummaryResult(
            summary=(
                "This report summarises the current certification readiness based on "
                "uploaded requirements, test cases, and evidence records. "
                "All AI-generated content requires human review before use in formal submissions."
            )
        )
