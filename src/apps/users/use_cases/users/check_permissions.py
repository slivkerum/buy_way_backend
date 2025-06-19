from http import HTTPStatus

from ninja.errors import HttpError

from apps.users.entities.users import UserRole

DENIED_ROLES = {UserRole.CUSTOMER, UserRole.SUPPORT}

def check_permissions(user) -> None:
    if user.role in DENIED_ROLES:
        raise HttpError(HTTPStatus.FORBIDDEN, "Недостаточно прав для выполнения действия")
