from dataclasses import dataclass
from typing import Optional


@dataclass
class OrganizationDocumentsEntity:
    id: int
    name: str

    path: str


@dataclass
class OrganizationEntity:
    id: int
    name: str

    is_active: bool
    documents: Optional[list['OrganizationDocumentsEntity']] = None