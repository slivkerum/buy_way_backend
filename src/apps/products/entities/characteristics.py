from dataclasses import dataclass


@dataclass
class CharacteristicEntity:
    id: int
    title: str
    options: list["CharacteristicOptionEntity"]

    @property
    def option_titles(self):
        return [option.title for option in self.options]


@dataclass
class CharacteristicOptionEntity:
    id: int
    title: str
