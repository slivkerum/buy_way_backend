from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.products.services.characteristics import BaseCharacteristicService
from config.containers import get_container
from api.v1.serializers.characteristics import CharacteristicSerializer


class CharacteristicListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        container = get_container()
        service: BaseCharacteristicService = container.resolve(BaseCharacteristicService)

        characteristics = service.get_all_characteristic()
        data = [CharacteristicSerializer.from_entity(char) for char in characteristics]
        return Response(data, status=status.HTTP_200_OK)


class CharacteristicDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, char_id: int):
        container = get_container()
        service: BaseCharacteristicService = container.resolve(BaseCharacteristicService)

        try:
            char = service.get_characteristic_by_id(char_id)
            data = CharacteristicSerializer.from_entity(char)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
