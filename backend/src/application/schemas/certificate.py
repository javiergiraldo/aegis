from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SSLCertificatePolicyBase(BaseModel):
    domain_name: str = Field(..., max_length=255)
    provider: str = "letsencrypt"
    challenge_type: str = "dns-01"
    expiration_date: datetime
    auto_renew_days_before: int = 30
    status: str = "active"

class SSLCertificatePolicyCreate(SSLCertificatePolicyBase):
    pass

class SSLCertificatePolicyResponse(SSLCertificatePolicyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
