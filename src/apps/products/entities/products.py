from uuid import UUID

from typing import List
from dataclasses import dataclass
from .categories import CategoryEntity
from .characteristics import CharacteristicOptionEntity


@dataclass
class ProductEntity:
    id: UUID
    title: str
    amount: float
    description: str
    category: CategoryEntity
    product_characteristic: List[CharacteristicOptionEntity]

    @property
    def characteristic_titles(self):
        return [char_option.title for char_option in self.product_characteristic]
