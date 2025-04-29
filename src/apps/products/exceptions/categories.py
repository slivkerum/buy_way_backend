from dataclasses import dataclass

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CategoryNotFound(ServiceException):
    id: int

    @property
    def message(self):
        return f"Продукт с таким id: {self.id} не найден"