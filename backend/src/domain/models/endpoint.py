import uuid
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, AuditableEntity, SoftDeleteEntity

class EndpointNode(Base, AuditableEntity, SoftDeleteEntity):
    __tablename__ = "endpoint_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    cluster_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="healthy")
    metadata_config: Mapped[dict] = mapped_column(JSON, nullable=True)
