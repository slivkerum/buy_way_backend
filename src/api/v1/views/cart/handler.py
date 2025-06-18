from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from config.containers import get_container

from apps.products.services.cart import BaseCartService
from apps.users.services.users import BaseUserService
from api.v1.serializers.cart import CartSerializer, CartProductSerializer


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение корзины текущего пользователя",
        responses={200: CartSerializer}
    )
    def get(self, request):
        user_id = request.user.id
        container = get_container()
        service: BaseCartService = container.resolve(BaseCartService)
        cart = service.get_cart_by_user(user_id)

        if not cart:
            return Response({"detail": "Корзина не найдена."}, status=status.HTTP_404_NOT_FOUND)

        serialized = CartSerializer.from_entity(cart)
        return Response(serialized)

    @swagger_auto_schema(
        request_body=CartSerializer,
        operation_description="Создание корзины для текущего пользователя",
        responses={201: CartSerializer},
        examples=[
            {
                "products": [
                    {
                        "product_id": "a1e8d0c6-8a7e-4ec4-a8e6-1846f33f6d92",
                        "quantity": 2
                    }
                ],
                "total_price": "1999.99"
            }
        ]
    )
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        container = get_container()
        service: BaseCartService = container.resolve(BaseCartService)

        created = service.create_cart(user_id)

        return Response(CartSerializer.from_entity(created), status=status.HTTP_201_CREATED)


class CartProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class: CartProductSerializer = CartProductSerializer

    @swagger_auto_schema(
        request_body=CartProductSerializer,
        operation_description="Добавление товара в корзину",
        responses={201: CartProductSerializer}
    )
    def post(self, request):
        container = get_container()
        cart_service: BaseCartService = container.resolve(BaseCartService)

        cart_id = self.get_cart_id(request)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity"))

        cart_product = cart_service.add_product_to_cart(cart_id, product_id, quantity)
        serialized = CartProductSerializer.from_entity(cart_product)
        return Response(serialized, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=CartProductSerializer,
        operation_description="Обновление количества товара в корзине",
        responses={200: CartProductSerializer}
    )
    def put(self, request):
        container = get_container()
        service: BaseCartService = container.resolve(BaseCartService)

        cart_id = self.get_cart_id(request)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity"))

        cart_product = service.update_product_quantity_in_cart(cart_id, product_id, quantity)
        serialized = CartProductSerializer.from_entity(cart_product)
        return Response(serialized)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["product_id"],
            properties={
                "product_id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid")
            },
            example={"product_id": "a1e8d0c6-8a7e-4ec4-a8e6-1846f33f6d92"}
        ),
        operation_description="Удаление товара из корзины",
        responses={204: "No Content"}
    )
    def delete(self, request):
        cart_id = self.get_cart_id(request)
        product_id = request.data.get("product_id")

        container = get_container()
        service: BaseCartService = container.resolve(BaseCartService)

        service.remove_product_from_cart(cart_id, product_id)
        return Response({"detail": "Товар удалён из корзины."}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_cart_id(request):
        container = get_container()
        cart_service: BaseCartService = container.resolve(BaseCartService)
        user_service: BaseUserService = container.resolve(BaseUserService)

        user = user_service.get_user_by_email(request.user)

        return cart_service.get_cart_by_user(user.id).id
