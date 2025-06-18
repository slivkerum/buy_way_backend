from http import HTTPStatus

from django.http import HttpRequest
from ninja import (
    Router,
)
from ninja.errors import HttpError
from ninja.security import HttpBearer

from api.schemas import ApiResponse
from api.v1.users.schemas import (
    CredentialsRequestSchema,
    RefreshTokenRequestSchema,
    TokenResponseSchema,
)
from apps.common.exceptions import ServiceException
from apps.users.exceptions.users import (
    UserEmailNotFound,
    UserInvalidCredentialsException,
)
from apps.users.use_cases.auth.authenticate import AuthenticateUseCase
from apps.users.use_cases.tokens.get import GetTokenPairUseCase
from apps.users.use_cases.tokens.refresh import RefreshTokenUseCase
from apps.users.use_cases.tokens.revoke import RevokeTokenUseCase
from config.containers import get_container


router = Router(tags=['Пользователи'])


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        container = get_container()
        use_case: AuthenticateUseCase = container.resolve(AuthenticateUseCase)

        try:
            user = use_case.execute(token)
        except ServiceException as e:
            raise HttpError(status_code=HTTPStatus.UNAUTHORIZED, message=e.message)

        request.user = user
        return token


@router.post('login/', response={HTTPStatus.OK: ApiResponse[TokenResponseSchema]})
def login(request: HttpRequest, credentials: CredentialsRequestSchema) -> ApiResponse[TokenResponseSchema]:
    """Выдает связку токенов (ACCESS, REFRESH)"""
    container = get_container()
    use_case: GetTokenPairUseCase = container.resolve(GetTokenPairUseCase)

    try:
        tokens, user = use_case.execute(credentials.email, credentials.password)
    except UserInvalidCredentialsException as e:
        raise HttpError(status_code=HTTPStatus.UNAUTHORIZED, message=e.message)
    except UserEmailNotFound as e:
        raise HttpError(status_code=HTTPStatus.NOT_FOUND, message=e.message)

    return ApiResponse(data=TokenResponseSchema.from_entity(tokens, user))


@router.post('refresh/', response={HTTPStatus.OK: ApiResponse[TokenResponseSchema]})
def refresh(
        request: HttpRequest,
        schema: RefreshTokenRequestSchema,
) -> ApiResponse[TokenResponseSchema]:
    """Обновляет связку токенов (ACCESS, REFRESH)"""

    container = get_container()
    use_case: RefreshTokenUseCase = container.resolve(RefreshTokenUseCase)

    try:
        tokens, user = use_case.execute(schema.refresh_token)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.UNAUTHORIZED, message=e.message)

    return ApiResponse(data=TokenResponseSchema.from_entity(tokens, user))


@router.post('revoke/', response={HTTPStatus.OK: ApiResponse})
def revoke(
        request: HttpRequest,
        schema: RefreshTokenRequestSchema,
):
    """Отзывает REFRESH токен."""
    container = get_container()
    use_case: RevokeTokenUseCase = container.resolve(RevokeTokenUseCase)

    try:
        use_case.execute(schema.refresh_token)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data=None)
