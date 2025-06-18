from dataclasses import dataclass

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class IncorrectTokenValueException(ServiceException):
    token: str

    @property
    def message(self):
        return f'Передан некорректный токен: {self.token}'


@dataclass(eq=False)
class TokenExpiredException(ServiceException):

    @property
    def message(self):
        return 'Переданный токен истек'


@dataclass(eq=False)
class TokenIncorrectTypeException(ServiceException):
    needed_type: str

    @property
    def message(self):
        return f'Переданный токен не является типом {self.needed_type}'


@dataclass(eq=False)
class TokenRevokedException(ServiceException):

    @property
    def message(self):
        return 'Переданный токен был отозван и не может быть использован'
