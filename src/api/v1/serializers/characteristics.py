from rest_framework import serializers
from apps.products.entities.characteristics import CharacteristicEntity


class CharacteristicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    option_titles = serializers.ListField(child=serializers.CharField())

    @staticmethod
    def from_entity(entity: CharacteristicEntity) -> dict:
        return {
            "id": entity.id,
            "title": entity.title,
            "option_titles": entity.option_titles,
        }
