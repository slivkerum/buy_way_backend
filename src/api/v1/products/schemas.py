from pydantic import BaseModel
from uuid import UUID

from apps.products.entities.categories import CategoryEntity
from apps.products.entities.characteristics import CharacteristicOptionEntity
from apps.products.entities.products import ProductEntity


class ProductRequestSchema(BaseModel):
    title: str
    amount: float
    description: str
    category_id: int
    characteristic_ids: list[int]

    def to_entity(self, product_id: UUID = None) -> ProductEntity:
        return ProductEntity(
            id=product_id,
            title=self.title,
            amount=self.amount,
            description=self.description,
            category=CategoryEntity(
                id=self.category_id,
                title="",
                parent_category_id=None,
                subcategories=[],
                characteristics=[]
            ),
            product_characteristic=[
                CharacteristicOptionEntity(id=cid, title="") for cid in self.characteristic_ids
            ]
        )


class ProductResponseSchema(BaseModel):
    id: UUID
    title: str
    amount: float
    description: str
    category_id: int
    characteristic_ids: list[int]

    @classmethod
    def from_entity(cls, entity: ProductEntity) -> 'ProductResponseSchema':
        return cls(
            id=entity.id,
            title=entity.title,
            amount=entity.amount,
            description=entity.description,
            category_id=entity.category.id,
            characteristic_ids=[c.id for c in entity.product_characteristic]
        )