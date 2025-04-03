from dataclasses import dataclass
from uuid import UUID


@dataclass
class MainCategoryEntity:
    id: UUID
    title: str
