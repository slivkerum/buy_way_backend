from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, conint

from apps.products.entities.reviews import ReviewEntity


class ReviewRequestSchema(BaseModel):
    product_id: UUID
    rating: conint(ge=1, le=5) = Field(..., description="Оценка от 1 до 5")
    text: str

    def to_entity(self, user_id: UUID) -> ReviewEntity:
        return ReviewEntity(
            id=None,
            user_id=user_id,
            product_id=self.product_id,
            rating=self.rating,
            text=self.text,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


class ReviewResponseSchema(BaseModel):
    id: int
    user_id: UUID
    product_id: UUID
    rating: int
    text: str

    @classmethod
    def from_entity(cls, entity: ReviewEntity) -> "ReviewResponseSchema":
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            product_id=entity.product_id,
            rating=entity.rating,
            text=entity.text,
        )
