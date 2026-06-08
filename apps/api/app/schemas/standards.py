from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.standards import StandardType


class StandardRead(BaseModel):
    id: UUID
    name: str
    standard_type: StandardType
    version: Optional[str]
    description: Optional[str]

    model_config = {"from_attributes": True}


class StandardClauseRead(BaseModel):
    id: UUID
    standard_id: UUID
    clause_id: str
    title: str
    description: Optional[str]
    is_mandatory: bool

    model_config = {"from_attributes": True}


class RequirementStandardLinkRead(BaseModel):
    id: UUID
    requirement_id: UUID
    standard_clause_id: UUID
    coverage_status: str
    notes: Optional[str]

    model_config = {"from_attributes": True}


class StandardCoverageResponse(BaseModel):
    standard_id: Optional[UUID]
    standard_name: str
    total_clauses: int
    covered_clauses: int
    coverage_percent: float
    missing_clauses: List[str]
    note: Optional[str] = None
