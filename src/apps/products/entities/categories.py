from typing import List, Optional
from dataclasses import dataclass
from .characteristics import CharacteristicEntity


@dataclass
class CategoryEntity:
    id: int
    title: str
    parent_category_id: Optional[int]
    subcategories: List["CategoryEntity"]
    characteristics: List[CharacteristicEntity]

    @property
    def subcategory_titles(self):
        return [subcategory.title for subcategory in self.subcategories]

    @property
    def characteristic_titles(self):
        return [characteristic.title for characteristic in self.characteristics]
