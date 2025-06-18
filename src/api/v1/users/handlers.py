from http import HTTPStatus
from pickle import FALSE
from uuid import UUID

from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError
from ninja.security import HttpBearer

from api.schemas import ApiResponse
from api.v1.users.filters import UserFilters
from api.v1.users.schemas import (
    CredentialsRequestSchema,
    RefreshTokenRequestSchema,
    TokenResponseSchema,
    UserRegistrationRequestSchema, UserResponseSchema, ConfirmationRequestSchema,
)
from apps.common.exceptions import ServiceException
from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import (
    UserEmailNotFound,
    UserInvalidCredentialsException,
)
from apps.users.models import User
from apps.users.services.users import BaseUserService
from apps.users.use_cases.auth.authenticate import AuthenticateUseCase
from apps.users.use_cases.tokens.get import GetTokenPairUseCase
from apps.users.use_cases.tokens.refresh import RefreshTokenUseCase
from apps.users.use_cases.tokens.revoke import RevokeTokenUseCase
from apps.users.use_cases.users.create import CreateUserUseCase
from apps.users.use_cases.users.email_confirmation.confirm import ConfirmEmailCodeUseCase
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


@router.post('registration/', response={HTTPStatus.CREATED: UserResponseSchema})
def registration(
        request: HttpRequest,
        schema: UserRegistrationRequestSchema,
) -> UserResponseSchema:
    """Регистрация пользователя"""
    container = get_container()
    use_case: CreateUserUseCase = container.resolve(CreateUserUseCase)

    try:
        user = use_case.execute(
            email=schema.email,
            password=schema.password,
            first_name=schema.first_name,
            last_name=schema.last_name,
            role=schema.role,
            organization=schema.organization,
            phone=schema.phone,
        )
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return UserResponseSchema.from_entity(user)


@router.post('confirm_email/', response={HTTPStatus.OK: ApiResponse})
def confirm_email(
        request: HttpRequest,
        schema: ConfirmationRequestSchema,
) -> ApiResponse:
    """Подтверждение почты"""
    container = get_container()
    use_case: ConfirmEmailCodeUseCase = container.resolve(ConfirmEmailCodeUseCase)

    try:
        use_case.execute(
            email=schema.email,
            code=schema.code,
        )
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data=None)


@router.get('', response={HTTPStatus.OK: UserResponseSchema}, auth=AuthBearer())
def get_user_by_email(request: HttpRequest) -> UserResponseSchema:
    """Получить текущего авторизованного пользователя"""
    container = get_container()
    user_service: BaseUserService = container.resolve(BaseUserService)

    try:
        user_entity = user_service.get_user_by_id(request.user.id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return UserResponseSchema.from_entity(user_entity)
