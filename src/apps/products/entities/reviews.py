from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ReviewEntity:
    id: int
    user_id: UUID
    product_id: UUID
    rating: int
    text: str
    created_at: datetime
    updated_at: datetime
