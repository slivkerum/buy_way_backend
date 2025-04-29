from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from config.containers import get_container

from apps.products.services.cart import BaseCartService
from apps.users.services.users import BaseUserService
from api.v1.serializers.cart import CartSerializer, CartProductSerializer


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        user_id = request.user.id
        container = get_container()
        service: BaseCartService = container.resolve(BaseCartService)
        cart = service.get_cart_by_user(user_id)

        if not cart:
            return Response({"detail": "Корзина не найдена."}, status=status.HTTP_404_NOT_FOUND)

        serialized = CartSerializer.from_entity(cart)
        return Response(serialized)

    @staticmethod
    def post(request):
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

    def post(self, request):
        container = get_container()
        cart_service: BaseCartService = container.resolve(BaseCartService)

        cart_id = self.get_cart_id(request)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        cart_product = cart_service.add_product_to_cart(cart_id, product_id, quantity)
        serialized = CartProductSerializer.from_entity(cart_product)
        return Response(serialized, status=status.HTTP_201_CREATED)

    def put(self, request):
        container = get_container()
        service: BaseCartService = container.resolve(BaseCartService)

        cart_id = self.get_cart_id(request)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        cart_product = service.update_product_quantity_in_cart(cart_id, product_id, quantity)
        serialized = CartProductSerializer.from_entity(cart_product)
        return Response(serialized)


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
