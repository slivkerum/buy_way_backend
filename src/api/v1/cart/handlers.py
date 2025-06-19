from http import HTTPStatus
from uuid import UUID
from typing import List

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from api.schemas import ApiResponse
from api.v1.cart.schemas import (
    CartResponseSchema,
    CartProductResponseSchema,
    CartProductUpdateSchema,
)
from apps.common.exceptions import ServiceException
from apps.products.services.cart import BaseCartService
from config.containers import get_container
from api.v1.users.handlers import AuthBearer

router = Router(tags=["Корзина"])


@router.get("/", response={HTTPStatus.OK: CartResponseSchema}, auth=AuthBearer())
def get_cart(request: HttpRequest):
    """Получить корзину пользователя"""
    service: BaseCartService = get_container().resolve(BaseCartService)

    try:
        cart = service.get_cart_by_user(request.user.id)
    except ServiceException as e:
        try:
            cart = service.create_cart(request.user.id)
        except ServiceException as ce:
            raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=ce.message)

    return CartResponseSchema.from_entity(cart)


@router.get("/products/", response={HTTPStatus.OK: List[CartProductResponseSchema]}, auth=AuthBearer())
def get_cart_products(request: HttpRequest):
    """Получить список товаров в корзине"""
    service: BaseCartService = get_container().resolve(BaseCartService)

    try:
        cart = service.get_cart_by_user(request.user.id)
        products = service.get_products_in_cart(cart.id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return [CartProductResponseSchema.from_entity(p) for p in products]


@router.post("product/add/", response={HTTPStatus.CREATED: CartProductResponseSchema}, auth=AuthBearer())
def add_product_to_cart(request: HttpRequest, product_id: UUID, quantity: int):
    """Добавить товар в корзину"""
    service: BaseCartService = get_container().resolve(BaseCartService)

    try:
        cart = service.get_cart_by_user(request.user.id)
        cart_product = service.add_product_to_cart(cart.id, product_id, quantity)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return HTTPStatus.CREATED, CartProductResponseSchema.from_entity(cart_product)



@router.put("/update/", response={HTTPStatus.OK: CartProductResponseSchema}, auth=AuthBearer())
def update_product_quantity(request: HttpRequest, data: CartProductUpdateSchema):
    """Обновить количество товара в корзине"""
    service: BaseCartService = get_container().resolve(BaseCartService)

    try:
        cart = service.get_cart_by_user(request.user.id)
        cart_product = service.update_product_quantity_in_cart(cart.id, data.product_id, data.quantity)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return CartProductResponseSchema.from_entity(cart_product)


@router.delete("product/remove/", response={HTTPStatus.OK: ApiResponse}, auth=AuthBearer())
def remove_product_from_cart(request: HttpRequest, product_id: UUID):
    """Удалить товар из корзины"""
    service: BaseCartService = get_container().resolve(BaseCartService)

    try:
        cart = service.get_cart_by_user(request.user.id)
        service.remove_product_from_cart(cart.id, product_id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data={"message": "Товар удалён из корзины"})



@router.delete("/clear/", response={HTTPStatus.OK: ApiResponse}, auth=AuthBearer())
def clear_cart(request: HttpRequest):
    """Очистить корзину"""
    service: BaseCartService = get_container().resolve(BaseCartService)

    try:
        cart = service.get_cart_by_user(request.user.id)
        service.clear_cart(cart.id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data={"message": "Корзина очищена"})
