from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class EndpointNodeBase(BaseModel):
    name: str = Field(..., max_length=255)
    ip_address: str = Field(..., max_length=50)
    cluster_id: str = Field(..., max_length=100)
    status: str = "healthy"
    metadata_config: Optional[Dict[str, Any]] = None

class EndpointNodeCreate(EndpointNodeBase):
    pass

class EndpointNodeResponse(EndpointNodeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
