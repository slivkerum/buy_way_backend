from abc import ABC, abstractmethod
from uuid import UUID
from dataclasses import dataclass

from apps.products.entities.cart import CartProductEntity, CartEntity
from apps.products.repositories.cart import BaseCartRepository


class BaseCartService(ABC):
    @abstractmethod
    def get_cart_by_user(self, user_id: UUID) -> CartEntity:
        """Получить корзину пользователя по user_id."""
        ...

    @abstractmethod
    def create_cart(self, user_id: UUID) -> CartEntity:
        """Создать корзину для пользователя."""
        ...

    @abstractmethod
    def add_product_to_cart(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        """Добавить товар в корзину."""
        ...

    @abstractmethod
    def update_product_quantity_in_cart(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        """Обновить количество товара в корзине."""
        ...

    @abstractmethod
    def remove_product_from_cart(self, cart_id: int, product_id: UUID) -> None:
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
class CartService(BaseCartService):
    repository: BaseCartRepository

    def get_cart_by_user(self, user_id: UUID) -> CartEntity:
        return self.repository.get_by_user(user_id)

    def create_cart(self, user_id: UUID) -> CartEntity:
        return self.repository.create(user_id)

    def add_product_to_cart(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        return self.repository.add_product(cart_id, product_id, quantity)

    def update_product_quantity_in_cart(self, cart_id: int, product_id: UUID, quantity: int) -> CartProductEntity:
        return self.repository.update_product_quantity(cart_id, product_id, quantity)

    def remove_product_from_cart(self, cart_id: int, product_id: UUID) -> None:
        return self.repository.remove_product(cart_id, product_id)

    def get_products_in_cart(self, cart_id: int) -> list[CartProductEntity]:
        return self.repository.get_products_in_cart(cart_id)

    def clear_cart(self, cart_id: int) -> None:
        return self.repository.clear_cart(cart_id)
