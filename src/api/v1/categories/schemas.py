from pydantic import BaseModel
from typing import Optional


class CategoryResponseSchema(BaseModel):
    id: int
    title: str
    parent_category_id: Optional[int] = None
    subcategories: list["CategoryResponseSchema"] = []
    characteristics: list[str] = []

    @classmethod
    def from_entity(cls, entity) -> "CategoryResponseSchema":
        return cls(
            id=entity.id,
            title=entity.title,
            parent_category_id=entity.parent_category_id,
            subcategories=[cls.from_entity(sub) for sub in entity.subcategories],
            characteristics=[c.title for c in entity.characteristics]
        )


CategoryResponseSchema.update_forward_refs()
