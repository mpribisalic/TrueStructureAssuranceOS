from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.project import CriticalityLevel, Industry, ProjectStatus


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    industry: Industry = Industry.other
    system_type: Optional[str] = None
    criticality_level: CriticalityLevel = CriticalityLevel.medium


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[Industry] = None
    system_type: Optional[str] = None
    criticality_level: Optional[CriticalityLevel] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: Optional[str]
    industry: Industry
    system_type: Optional[str]
    criticality_level: CriticalityLevel
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
