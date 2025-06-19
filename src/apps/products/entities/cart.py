from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CartProductEntity:
    id: int
    product_id: UUID
    quantity: int


@dataclass
class CartEntity:
    id: int
    user_id: UUID
    total_price: int
    created_at: datetime
    items: list[CartProductEntity]
