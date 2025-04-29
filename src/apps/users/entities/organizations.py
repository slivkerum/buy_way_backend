from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class OrganizationEntity:
    id: int
    name: str
    owner_id: UUID
    created_at: datetime
    documents_path: list[str]
    is_active: bool