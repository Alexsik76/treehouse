import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, field_validator
from src.models.infrastructure import InfrastructureType


# Base schema with common fields (no strict validation here to allow reading legacy data)
class InfrastructureItemBase(BaseModel):
    name: str
    type: InfrastructureType
    ip_address: Optional[str] = None
    dns_name: Optional[str] = None
    specs: Dict[str, Any] = {}
    parent_id: Optional[int] = None

# Validation Mixin for Create/Update
class ValidationMixin:
    @field_validator('ip_address')
    @classmethod
    def validate_ip(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        # Basic IPv4 validation
        ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ipv4_pattern.match(v):
            raise ValueError('Invalid IP address format')
        return v

    @field_validator('dns_name')
    @classmethod
    def validate_dns(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        # Simple hostname validation
        dns_pattern = re.compile(r'^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(\.[a-zA-Z0-9-]{1,63})*$')
        if not dns_pattern.match(v):
            raise ValueError('Invalid DNS name format')
        return v

class InfrastructureItemCreate(InfrastructureItemBase, ValidationMixin):
    pass

class InfrastructureItemUpdate(BaseModel, ValidationMixin):
    name: Optional[str] = None
    type: Optional[InfrastructureType] = None
    ip_address: Optional[str] = None
    dns_name: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None

class InfrastructureItemResponse(InfrastructureItemBase):
    id: int
    children: List['InfrastructureItemResponse'] = []

    model_config = ConfigDict(from_attributes=True)
