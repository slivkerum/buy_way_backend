from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.products.services.products import BaseProductService
from config.containers import get_container
from api.v1.serializers.products import ProductSerializer


class ProductListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        container = get_container()
        service: BaseProductService = container.resolve(BaseProductService)
        products = service.get_all()

        serialized = [ProductSerializer.from_entity(p) for p in products]
        return Response(serialized)

    @staticmethod
    def post(request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        container = get_container()
        service: BaseProductService = container.resolve(BaseProductService)

        product_entity = serializer.to_entity()
        created = service.create_product(product_entity)

        return Response(ProductSerializer.from_entity(created), status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, product_id: UUID):
        container = get_container()
        service: BaseProductService = container.resolve(BaseProductService)

        try:
            product = service.get_product(product_id)
            return Response(ProductSerializer.from_entity(product))
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def put(request, product_id: UUID):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        container = get_container()
        service: BaseProductService = container.resolve(BaseProductService)

        updated_entity = serializer.to_entity()
        updated_entity.id = product_id
        updated = service.update_product(updated_entity)

        return Response(ProductSerializer.from_entity(updated))

    @staticmethod
    def delete(request, product_id: UUID):
        container = get_container()
        service: BaseProductService = container.resolve(BaseProductService)

        service.delete_product(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
