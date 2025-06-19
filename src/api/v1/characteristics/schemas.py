from pydantic import BaseModel
from typing import List


class CharacteristicOptionSchema(BaseModel):
    id: int
    title: str


class CharacteristicResponseSchema(BaseModel):
    id: int
    title: str
    options: List[CharacteristicOptionSchema]

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            title=entity.title,
            options=[
                CharacteristicOptionSchema(id=opt.id, title=opt.title)
                for opt in entity.options
            ]
        )
