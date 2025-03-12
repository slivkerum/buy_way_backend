from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    ADMIN = 'Администратор'
    CUSTOMER = 'Покупатель'
    SELLER = 'Продавец'
    SUPPORT = 'Тех .поддержка'


@dataclass
class UserEntity:
    id: UUID
    first_name: str
    last_name: str

    email: str
    password: str

    role: UserRole

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'