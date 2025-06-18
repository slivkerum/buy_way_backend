from dataclasses import dataclass
from uuid import UUID

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class UserEmailNotFound(ServiceException):
    email: str

    @property
    def message(self):
        return f'Пользователь с переданным email не найден: {self.email}'


@dataclass(eq=False)
class UserEmailAlreadyExistsException(ServiceException):

    @property
    def message(self):
        return f'Такой email уже существует'


@dataclass(eq=False)
class UserIdNotFound(ServiceException):
    user_id: UUID

    @property
    def message(self):
        return f'Пользователь с переданным id не найден: {self.user_id}'


@dataclass(eq=False)
class UserInvalidCredentialsException(ServiceException):

    @property
    def message(self):
        return 'Неверный логин или пароль'


@dataclass(eq=False)
class UserNotActiveException(ServiceException):

    @property
    def message(self):
        return 'Пользователь неактивен'


@dataclass(eq=False)
class UserIncorrectRoleException(ServiceException):

    @property
    def message(self):
        return 'У вас нет прав для просмотра содержимого'
