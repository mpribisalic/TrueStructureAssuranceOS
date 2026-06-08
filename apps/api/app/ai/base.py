"""AI provider interface — all providers must implement this ABC."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExtractedRequirement:
    external_id: str
    title: str
    text: str
    category: str = "functional"
    criticality: str = "medium"
    verification_method: str = "test"
    confidence: float = 0.0
    source_reference: str = ""


@dataclass
class RequirementExtractionResult:
    requirements: list[ExtractedRequirement] = field(default_factory=list)


@dataclass
class SuggestedLink:
    requirement_external_id: str
    test_case_external_id: str
    link_type: str = "verifies"
    confidence: float = 0.0
    reason: str = ""


@dataclass
class TraceSuggestionResult:
    links: list[SuggestedLink] = field(default_factory=list)


@dataclass
class GapExplanationResult:
    summary: str = ""
    recommended_actions: list[str] = field(default_factory=list)


@dataclass
class ReportSummaryResult:
    summary: str = ""


class AIProvider(ABC):
    @abstractmethod
    def extract_requirements(self, text: str) -> RequirementExtractionResult: ...

    @abstractmethod
    def suggest_trace_links(self, requirements, test_cases, evidence) -> TraceSuggestionResult: ...

    @abstractmethod
    def explain_gaps(self, gaps) -> GapExplanationResult: ...

    @abstractmethod
    def generate_report_summary(self, context) -> ReportSummaryResult: ...
