from dataclasses import dataclass
from uuid import UUID

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class UserIdNotFound(ServiceException):
    id: UUID

    @property
    def message(self):
        return f"Пользователь с таким id: {self.id} не найден"


@dataclass(eq=False)
class UserEmailNotFound(ServiceException):
    email: str

    @property
    def message(self):
        return f"Пользователь с таки email: {self.email} не найден"
