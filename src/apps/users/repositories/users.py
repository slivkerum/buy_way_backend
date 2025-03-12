from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from django.contrib.auth.hashers import check_password

from apps.users.models.users import User
from apps.users.entities.users import (
    UserEntity,
)
from apps.users.exceptions.users import (
    UserIdNotFound,
    UserEmailNotFound
)


class BaseUserRepository(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> UserEntity:...

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity:...

    @abstractmethod
    def compare_password(self, given_password: str, user_password: str) -> bool:...

    @abstractmethod
    def create_user(self, user: UserEntity) -> None:...


class UserRepository(BaseUserRepository):

    def get_user_by_id(self, user_id: UUID) -> UserEntity:
        user = User.objects.filter(id=user_id)
        if not user:
            raise UserIdNotFound(user_id)
        return user.first().to_entity()

    def get_user_by_email(self, email: str) -> UserEntity:
        user = User.objects.filter(email=email)
        if not user:
            raise UserEmailNotFound(email)
        return user.first().to_entity()

    def compare_password(self, given_password: str, user_password: str) -> bool:
        return check_password(given_password, user_password)

    def create_user(self, user: UserEntity) -> None:
        User.objects.create_user(
            first_name=user.first_name,
            last_name=user.last_name,

            email=user.email,
            password=user.password,
            role=user.role,
        )
