import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import AuditableEntity, Base, SoftDeleteEntity


class SSLCertificatePolicy(Base, AuditableEntity, SoftDeleteEntity):
    __tablename__ = "ssl_certificate_policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False, default="letsencrypt")
    challenge_type: Mapped[str] = mapped_column(String(50), nullable=False, default="dns-01")
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    auto_renew_days_before: Mapped[int] = mapped_column(Integer, default=30)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
