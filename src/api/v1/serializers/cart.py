from rest_framework import serializers
from apps.products.entities.cart import CartEntity, CartProductEntity


class CartProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def to_entity(self) -> CartProductEntity:
        return CartProductEntity(
            id=self.validated_data["id"],
            product_id=self.validated_data["product_id"],
            quantity=self.validated_data["quantity"]
        )

    @staticmethod
    def from_entity(cart_product: CartProductEntity) -> dict:
        return {
            "product_id": cart_product.product_id,
            "quantity": cart_product.quantity
        }


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    products = CartProductSerializer(many=True, required=False)

    def to_entity(self) -> CartEntity:
        return CartEntity(
            id=self.validated_data.get("id"),
            user_id=self.validated_data["user_id"],
            items=[CartProductEntity(**product) for product in self.validated_data.get("items", [])],
            created_at=self.validated_data.get("created_at")
        )

    @staticmethod
    def from_entity(cart: CartEntity) -> dict:
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": [CartProductSerializer.from_entity(product) for product in cart.items]
        }
