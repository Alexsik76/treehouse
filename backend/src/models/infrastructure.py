import enum
from typing import List, Optional

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class InfrastructureType(str, enum.Enum):
    SERVER = "server"
    VM = "vm"
    CONTAINER = "container"
    SWITCH = "switch"
    ROUTER = "router"
    OTHER = "other"

class InfrastructureItem(Base):
    __tablename__ = "infrastructure_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[InfrastructureType] = mapped_column(
        SAEnum(InfrastructureType, native_enum=False), 
        nullable=False
    )
    # Using String for IP for simplicity, though INET is better for Postgres
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dns_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # JSONB field for flexible specs (OS, RAM, Disk, etc.)
    specs: Mapped[dict] = mapped_column(JSONB, default={}, server_default='{}')

    # Self-referential relationship
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("infrastructure_items.id"), nullable=True)
    
    # Relationships
    parent: Mapped[Optional['InfrastructureItem']] = relationship("InfrastructureItem", remote_side=[id], back_populates="children")
    children: Mapped[List['InfrastructureItem']] = relationship("InfrastructureItem", back_populates="parent", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InfrastructureItem(id={self.id}, name='{self.name}', type='{self.type}')>"
