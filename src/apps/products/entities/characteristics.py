from typing import List
from dataclasses import dataclass


@dataclass
class CharacteristicEntity:
    id: int
    title: str
    options: List["CharacteristicOptionEntity"]

    @property
    def option_titles(self):
        return [option.title for option in self.options]


@dataclass
class CharacteristicOptionEntity:
    id: int
    title: str
