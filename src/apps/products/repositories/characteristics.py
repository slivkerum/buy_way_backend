from abc import ABC, abstractmethod
from typing import List
from apps.products.models.characteristics import Characteristic
from apps.products.entities.characteristics import CharacteristicEntity
from apps.products.exceptions.characteristics import CharacteristicNotFound


class BaseCharacteristicRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[CharacteristicEntity]: ...

    @abstractmethod
    def get_by_id(self, char_id: int) -> CharacteristicEntity: ...


class CharacteristicRepository(BaseCharacteristicRepository):

    def get_all(self) -> List[CharacteristicEntity]:
        return [char.to_entity() for char in Characteristic.objects.all()]

    def get_by_id(self, char_id: int) -> CharacteristicEntity:
        char = Characteristic.objects.filter(id=char_id).first()
        if not char:
            raise CharacteristicNotFound(char_id)
        return char.to_entity()
