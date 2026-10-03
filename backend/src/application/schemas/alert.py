from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from src.domain.models.alert import AlertSeverity

class SecurityAlertBase(BaseModel):
    source_ip: str = Field(..., max_length=50)
    severity: AlertSeverity
    alert_type: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    payload: Optional[Dict[str, Any]] = None

class SecurityAlertCreate(SecurityAlertBase):
    pass

class SecurityAlertResponse(SecurityAlertBase):
    id: UUID
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
