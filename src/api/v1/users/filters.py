from typing import Optional

from ninja import Schema

from apps.users.filters.users import UserFilters as UserFiltersEntity


class UserFilters(Schema):
    is_active: bool
    role: str

    def to_entity(self) -> UserFiltersEntity:
        return UserFiltersEntity(
            is_active=self.is_active,
            role=self.role,
        )
