from abc import ABC, abstractmethod
from uuid import UUID
from dataclasses import dataclass

from apps.products.models import Cart, CartProduct
from apps.products.entities.cart import CartProductEntity, CartEntity

class BaseCartRepository(ABC):

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> CartEntity:
        """Получить корзину пользователя по user_id."""
        ...

    @abstractmethod
    def create(self, user_id: UUID) -> CartEntity:
        """Создать корзину для пользователя."""
        ...

    @abstractmethod
    def add_product(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        """Добавить товар в корзину."""
        ...

    @abstractmethod
    def update_product_quantity(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        """Обновить количество товара в корзине."""
        ...

    @abstractmethod
    def remove_product(self, cart_id: int, product_id: UUID) -> None:
        """Удалить товар из корзины."""
        ...

    @abstractmethod
    def get_products_in_cart(self, cart_id: int) -> list[CartProductEntity]:
        """Получить список товаров в корзине."""
        ...

    @abstractmethod
    def clear_cart(self, cart_id: int) -> None:
        """Очистить корзину."""
        ...


@dataclass
class CartRepository(BaseCartRepository):

    def get_by_user(self, user_id: UUID) -> CartEntity:
        cart = Cart.objects.get(user_id=user_id)
        return cart.to_entity()

    def create(self, user_id: UUID) -> CartEntity:
        cart = Cart.objects.create(user_id=user_id)
        return cart.to_entity()

    def add_product(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        cart = Cart.objects.get(id=cart_id)

        if product_id in cart:
            self.update_product_quantity(cart_id, product_id, quantity)

        cart_product = CartProduct.objects.create(
            cart=cart,
            product_id=product_id,
            quantity=quantity
        )
        return cart_product.to_entity()

    def update_product_quantity(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        cart_product = CartProduct.objects.get(cart_id=cart_id, product_id=product_id)
        cart_product.quantity = quantity
        cart_product.save()
        return cart_product.to_entity()

    def remove_product(self, cart_id: int, product_id: UUID) -> None:
        cart_product = CartProduct.objects.get(cart_id=cart_id, product_id=product_id)
        cart_product.delete()

    def get_products_in_cart(self, cart_id: int) -> list[CartProductEntity]:
        cart_products = CartProduct.objects.filter(cart_id=cart_id)
        return [product.to_entity() for product in cart_products]

    def clear_cart(self, cart_id: int) -> None:
        CartProduct.objects.filter(cart_id=cart_id).delete()
