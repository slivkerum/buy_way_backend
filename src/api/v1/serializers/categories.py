from rest_framework import serializers

from apps.products.entities.categories import CategoryEntity


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    parent_category_id = serializers.IntegerField(required=False, allow_null=True)
    subcategory_titles = serializers.ListField(child=serializers.CharField())
    characteristic_titles = serializers.ListField(child=serializers.CharField())

    @staticmethod
    def from_entity(entity: CategoryEntity) -> dict:
        return {
            "id": entity.id,
            "title": entity.title,
            "parent_category_id": entity.parent_category_id,
            "subcategory_titles": entity.subcategory_titles,
            "characteristic_titles": entity.characteristic_titles,
        }
