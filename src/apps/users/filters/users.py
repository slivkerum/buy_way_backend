from dataclasses import dataclass

@dataclass
class UserFilters:
    is_active: bool | None = None
    role: str | None = None