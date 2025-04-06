from dataclasses import dataclass
from uuid import UUID

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ProductNotFound(ServiceException):
    id: UUID

    @property
    def message(self):
        return f"Продукт с таким id: {self.id} не найден"