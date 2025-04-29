from rest_framework import serializers
from uuid import uuid4

from apps.products.entities.products import ProductEntity
from apps.products.entities.categories import CategoryEntity
from apps.products.entities.characteristics import CharacteristicOptionEntity


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=256)
    amount = serializers.FloatField()
    description = serializers.CharField()
    category_id = serializers.IntegerField()
    characteristic_option_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    characteristics = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )
    category = serializers.CharField(read_only=True)

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            id=uuid4(),
            title=self.validated_data["title"],
            amount=self.validated_data["amount"],
            description=self.validated_data["description"],
            category=CategoryEntity(id=self.validated_data["category_id"], title="", parent_category_id=None, subcategories=[], characteristics=[]),
            product_characteristic=[
                CharacteristicOptionEntity(id=cid, title="") for cid in self.validated_data["characteristic_option_ids"]
            ]
        )

    @staticmethod
    def from_entity(product: ProductEntity) -> dict:
        return {
            "id": product.id,
            "title": product.title,
            "amount": product.amount,
            "description": product.description,
            "category": product.category.title if product.category else None,
            "characteristics": product.characteristic_titles,
        }
