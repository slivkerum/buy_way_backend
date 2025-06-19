from http import HTTPStatus
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from api.v1.users.handlers import AuthBearer
from config.containers import get_container
from apps.products.services.categories import BaseCategoryService
from api.v1.categories.schemas import CategoryResponseSchema

router = Router(tags=["Категории"])


@router.get("/", response={HTTPStatus.OK: list[CategoryResponseSchema]}, auth=AuthBearer())
def get_categories(request: HttpRequest):
    service: BaseCategoryService = get_container().resolve(BaseCategoryService)
    categories = service.get_all_categories()
    return [CategoryResponseSchema.from_entity(cat) for cat in categories]


@router.get("/{category_id}/", response={HTTPStatus.OK: CategoryResponseSchema}, auth=AuthBearer())
def get_category_by_id(request: HttpRequest, category_id: int):
    service: BaseCategoryService = get_container().resolve(BaseCategoryService)
    try:
        category = service.get_category_by_id(category_id)
    except Exception as e:
        raise HttpError(status_code=HTTPStatus.NOT_FOUND, message=str(e))
    return CategoryResponseSchema.from_entity(category)
