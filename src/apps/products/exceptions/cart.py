from dataclasses import dataclass
from uuid import UUID
from apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CartNotFound(ServiceException):
    cart_id: int

    @property
    def message(self):
        return f"Корзина для пользователя с ID {self.cart_id} не найдена"


@dataclass(eq=False)
class CartProductNotFound(ServiceException):
    product_id: UUID

    @property
    def message(self):
        return f"Товар с ID {self.product_id} не найден в корзине"


@dataclass(eq=False)
class CartIsEmpty(ServiceException):

    @property
    def message(self):
        return 'Корзина пуста, добавьте товары для продолжения'


@dataclass(eq=False)
class CartProductQuantityInvalid(ServiceException):
    product_id: UUID
    quantity: int

    @property
    def message(self):
        return f"Неверное количество товара с ID {self.product_id}: {self.quantity}. Количество должно быть положительным числом."
