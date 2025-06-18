from dataclasses import dataclass

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class DocumentNotFoundException(ServiceException):
    document_id: int

    @property
    def message(self):
        return f'Школа с id {self.document_id} не найдена'


@dataclass(eq=False)
class OrganizationNotFoundException(ServiceException):
    organization_name: int

    @property
    def message(self):
        return f'Данной организации {self.organization_name} не существует'