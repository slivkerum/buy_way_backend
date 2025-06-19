from http import HTTPStatus
from uuid import UUID

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from api.schemas import ApiResponse
from api.v1.users.handlers import AuthBearer
from apps.common.exceptions import ServiceException
from apps.products.services.products import BaseProductService
from apps.users.use_cases.users.check_permissions import check_permissions
from config.containers import get_container
from api.v1.products.schemas import ProductRequestSchema, ProductResponseSchema


router = Router(tags=["Товары"])


@router.get("/", response={HTTPStatus.OK: list[ProductResponseSchema]})
def list_products(request: HttpRequest):
    service: BaseProductService = get_container().resolve(BaseProductService)
    try:
        products = service.get_all()
    except ServiceException as e:
        raise HttpError(HTTPStatus.BAD_REQUEST, message=e.message)
    return products


@router.get("/{product_id}/", response={HTTPStatus.OK: ProductResponseSchema})
def get_product(request: HttpRequest, product_id: UUID):
    service: BaseProductService = get_container().resolve(BaseProductService)
    try:
        product = service.get_product(product_id)
    except ServiceException as e:
        raise HttpError(HTTPStatus.NOT_FOUND, message=e.message)
    return product


@router.post("/new/create/", response={HTTPStatus.CREATED: ProductResponseSchema}, auth=AuthBearer())
def create_product(request: HttpRequest, data: ProductRequestSchema):
    check_permissions(request.user)
    service: BaseProductService = get_container().resolve(BaseProductService)
    try:
        product = service.create_product(data.to_entity())
    except ServiceException as e:
        raise HttpError(HTTPStatus.BAD_REQUEST, message=e.message)
    return HTTPStatus.CREATED, ProductResponseSchema.from_entity(product)


@router.put("/update/{product_id}/", response={HTTPStatus.OK: ProductResponseSchema}, auth=AuthBearer())
def update_product(request: HttpRequest, product_id: UUID, data: ProductRequestSchema):
    check_permissions(request.user)
    service: BaseProductService = get_container().resolve(BaseProductService)
    try:
        product = service.update_product(data.to_entity(product_id=product_id))
    except ServiceException as e:
        raise HttpError(HTTPStatus.BAD_REQUEST, message=e.message)
    return ProductResponseSchema.from_entity(product)


@router.delete("/delete/{product_id}/", response={HTTPStatus.OK: ApiResponse}, auth=AuthBearer())
def delete_product(request: HttpRequest, product_id: UUID):
    check_permissions(request.user)
    service: BaseProductService = get_container().resolve(BaseProductService)
    try:
        service.delete_product(product_id)
    except ServiceException as e:
        raise HttpError(HTTPStatus.BAD_REQUEST, message=e.message)
    return ApiResponse(data={"message": "Продукт удалён"})
