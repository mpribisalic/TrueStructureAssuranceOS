"""Schemas for ATVP (Autonomous Test & Validation Platform) connector."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ATVPTestResult(BaseModel):
    test_id: str
    test_name: str
    status: str  # "PASSED", "FAILED", "ERROR"
    metric: Optional[str] = None
    expected: Optional[float] = None
    actual: Optional[float] = None
    score: Optional[float] = None
    timestamp: Optional[datetime] = None
    notes: Optional[str] = None


class ATVPImportRequest(BaseModel):
    platform: str = "ATVP"
    version: str = "1.0"
    export_timestamp: Optional[datetime] = None
    scenario: Optional[str] = None
    results: List[ATVPTestResult]


class ATVPImportResponse(BaseModel):
    imported: int
    skipped: int
    errors: List[str]
    evidence_ids: List[str]
    message: str
