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


@dataclass(eq=False)
class UserNotActiveException(ServiceException):

    @property
    def message(self):
        return 'Пользователь неактивен'


@dataclass(eq=False)
class UserInvalidCredentialsException(ServiceException):

    @property
    def message(self):
        return 'Неверный логин или пароль'


@dataclass(eq=False)
class UserEmailAlreadyExistsException(ServiceException):

    @property
    def message(self):
        return f'Пользователь с таким email уже существует'

