from dataclasses import dataclass
from uuid import UUID

from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ReviewNotFound(ServiceException):
    id: int

    @property
    def message(self):
        return f"Продукт с таким id: {self.id} не найден"