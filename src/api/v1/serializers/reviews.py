from rest_framework import serializers
from apps.products.entities.reviews import ReviewEntity
from uuid import UUID
from datetime import datetime


class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    @staticmethod
    def from_entity(entity: ReviewEntity) -> dict:
        return {
            "id": entity.id,
            "rating": entity.rating,
            "text": entity.text,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }

    def to_entity(self, product_id: UUID, user_id: UUID) -> ReviewEntity:
        now = datetime.utcnow()
        return ReviewEntity(
            id=0,
            user_id=user_id,
            product_id=product_id,
            rating=self.validated_data["rating"],
            text=self.validated_data["text"],
            created_at=now,
            updated_at=now
        )
