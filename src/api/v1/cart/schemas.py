from uuid import UUID
from pydantic import BaseModel

from apps.products.entities.cart import CartEntity, CartProductEntity


class CartProductResponseSchema(BaseModel):
    id: int
    product_id: UUID
    quantity: int

    @classmethod
    def from_entity(cls, entity: CartProductEntity) -> "CartProductResponseSchema":
        return cls(
            id=entity.id,
            product_id=entity.product_id,
            quantity=entity.quantity
        )


class CartResponseSchema(BaseModel):
    id: int
    user_id: UUID
    total_price: float
    items: list[CartProductResponseSchema]

    @classmethod
    def from_entity(cls, entity: CartEntity) -> 'CartResponseSchema':
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            total_price=entity.total_price,
            items=[
                CartProductResponseSchema.from_entity(item)
                for item in entity.items
            ]
        )


class CartProductUpdateSchema(BaseModel):
    product_id: UUID
    quantity: int
