from abc import ABC, abstractmethod
from uuid import UUID
from dataclasses import dataclass

from apps.products.models import Cart, CartProduct, Product
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

    @abstractmethod
    def _recalculate_cart_total(self, cart: Cart) -> None:
        """Пересчет итоговой суммы корзины"""
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

        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        self._recalculate_cart_total(cart)

        return cart_product.to_entity()

    def update_product_quantity(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        cart_product = CartProduct.objects.get(cart_id=cart_id, product_id=product_id)
        cart_product.quantity = quantity
        cart_product.save()
        self._recalculate_cart_total(cart_product.cart)

        return cart_product.to_entity()

    def remove_product(self, cart_id: int, product_id: UUID) -> None:
        cart_product = CartProduct.objects.get(cart_id=cart_id, product_id=product_id)
        cart = cart_product.cart
        cart_product.delete()
        self._recalculate_cart_total(cart)

    def get_products_in_cart(self, cart_id: int) -> list[CartProductEntity]:
        cart_products = CartProduct.objects.filter(cart_id=cart_id)
        return [product.to_entity() for product in cart_products]

    def clear_cart(self, cart_id: int) -> None:
        cart = Cart.objects.get(id=cart_id)
        CartProduct.objects.filter(cart=cart).delete()
        cart.total_price = 0
        cart.save(update_fields=["total_price"])

    def _recalculate_cart_total(self, cart: Cart) -> None:
        cart_items = CartProduct.objects.filter(cart=cart).select_related('product')
        total = 0

        for item in cart_items:
            product = item.product
            quantity = item.quantity
            total += product.final_price * quantity

        cart.total_price = total
        cart.save(update_fields=["total_price"])

