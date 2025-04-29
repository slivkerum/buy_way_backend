from dataclasses import dataclass

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class OrganizationNotFound(ServiceException):
    id: int

    @property
    def message(self):
        return f"Организация с ID {id} не найдена"

@dataclass(eq=False)
class InvalidAddFile(ServiceException):

    @property
    def message(self):
        return f"Ошибка добавления файла, попробуйте снова"