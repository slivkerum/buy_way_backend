from http import HTTPStatus
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from api.v1.users.handlers import AuthBearer
from config.containers import get_container
from apps.products.services.characteristics import BaseCharacteristicService
from api.v1.characteristics.schemas import CharacteristicResponseSchema

router = Router(tags=["Характеристики"])


@router.get("/", response={HTTPStatus.OK: list[CharacteristicResponseSchema]}, auth=AuthBearer())
def get_all_characteristics(request: HttpRequest):
    service: BaseCharacteristicService = get_container().resolve(BaseCharacteristicService)
    characteristics = service.get_all_characteristic()
    return [CharacteristicResponseSchema.from_entity(c) for c in characteristics]


@router.get("/{char_id}/", response={HTTPStatus.OK: CharacteristicResponseSchema}, auth=AuthBearer())
def get_characteristic_by_id(request: HttpRequest, char_id: int):
    service: BaseCharacteristicService = get_container().resolve(BaseCharacteristicService)
    try:
        char = service.get_characteristic_by_id(char_id)
    except Exception as e:
        raise HttpError(status_code=HTTPStatus.NOT_FOUND, message=str(e))
    return CharacteristicResponseSchema.from_entity(char)
