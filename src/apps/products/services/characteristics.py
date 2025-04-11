from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.products.repositories.characteristics import BaseCharacteristicRepository
from apps.products.entities.characteristics import CharacteristicEntity


class BaseCharacteristicService(ABC):

    @abstractmethod
    def get_all_characteristic(self) -> list[CharacteristicEntity]:
        ...

    @abstractmethod
    def get_characteristic_by_id(self, category_id: int) -> CharacteristicEntity:
        ...


@dataclass
class CharacteristicService(BaseCharacteristicService):
    repo: BaseCharacteristicRepository

    def get_all_characteristic(self) -> list[CharacteristicEntity]:
        return self.repo.get_all()

    def get_characteristic_by_id(self, characteristic_id: int) -> CharacteristicEntity:
        return self.repo.get_by_id(characteristic_id)
