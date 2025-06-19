from http import HTTPStatus
from uuid import UUID

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from api.schemas import ApiResponse
from api.v1.reviews.schemas import (
    ReviewRequestSchema,
    ReviewResponseSchema,
)
from apps.common.exceptions import ServiceException
from apps.products.services.reviews import BaseReviewService
from config.containers import get_container
from api.v1.users.handlers import AuthBearer

router = Router(tags=["Отзывы"])


@router.get("/product/{product_id}/", response={HTTPStatus.OK: list[ReviewResponseSchema]})
def get_reviews_by_product(request: HttpRequest, product_id: UUID):
    """Получить все отзывы по товару"""
    service: BaseReviewService = get_container().resolve(BaseReviewService)

    try:
        reviews = service.get_reviews_by_product(product_id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return [ReviewResponseSchema.from_entity(r) for r in reviews]


@router.get("/{review_id}/", response={HTTPStatus.OK: ReviewResponseSchema})
def get_review_by_id(request: HttpRequest, review_id: int):
    """Получить отзыв по его ID"""
    service: BaseReviewService = get_container().resolve(BaseReviewService)

    try:
        review = service.get_review_by_id(review_id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.NOT_FOUND, message=e.message)

    return ReviewResponseSchema.from_entity(review)


@router.post("/new/create/", response={HTTPStatus.CREATED: ReviewResponseSchema}, auth=AuthBearer())
def create_review(request: HttpRequest, data: ReviewRequestSchema):
    """Оставить отзыв (авторизованному пользователю)"""
    service: BaseReviewService = get_container().resolve(BaseReviewService)

    try:
        entity = data.to_entity(user_id=request.user.id)
        created = service.add_review(entity)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return HTTPStatus.CREATED, ReviewResponseSchema.from_entity(created)


@router.delete("/delete/{review_id}/", response={HTTPStatus.OK: ApiResponse}, auth=AuthBearer())
def delete_review(request: HttpRequest, review_id: int):
    """Удалить отзыв (если это твой)"""
    service: BaseReviewService = get_container().resolve(BaseReviewService)

    try:
        review = service.get_review_by_id(review_id)
        if review.user_id != request.user.id:
            raise HttpError(status_code=HTTPStatus.FORBIDDEN, message="Вы не можете удалить этот отзыв.")
        service.delete_review(review_id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data={"message": "Отзыв удалён"})
