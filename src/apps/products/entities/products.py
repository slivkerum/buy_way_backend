from uuid import UUID
from dataclasses import dataclass


@dataclass
class CharacteristicOptionEntity:
    id: int
    title: str


@dataclass
class CharacteristicEntity:
    id: int
    title: str
    options: list[CharacteristicOptionEntity]


@dataclass
class ProductCharacteristicEntity:
    characteristic: CharacteristicEntity
    selected_option: CharacteristicOptionEntity


@dataclass
class ProductEntity:
    id: UUID
    title: str
    amount: float
    description: str
    product_characteristic: list[ProductCharacteristicEntity]
