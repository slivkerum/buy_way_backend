from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    ADMIN = 'Администратор'
    CUSTOMER = 'Покупатель'
    SELLER = 'Продавец'
    SUPPORT = 'Тех.поддержка'


@dataclass
class UserEntity:
    id: UUID
    first_name: str
    last_name: str

    phone: str

    email: str
    password: str

    role: UserRole

    is_active: bool = False
    enters_count: int = 0

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'