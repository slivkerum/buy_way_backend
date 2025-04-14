from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from django.contrib.auth.hashers import check_password
from django.utils import timezone

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
    def update_user(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def create_user(self, user: UserEntity) -> None:...

    @abstractmethod
    def soft_delete_user(self, user: UserEntity) -> None:...


class UserRepository(BaseUserRepository):

    def get_user_by_id(self, user_id: UUID) -> UserEntity:
        user = User.objects.filter(id=user_id, is_deleted=False)
        if not user:
            raise UserIdNotFound(user_id)
        return user.first().to_entity()

    def get_user_by_email(self, email: str) -> UserEntity:
        user = User.objects.filter(email=email, is_deleted=False)
        if not user:
            raise UserEmailNotFound(email)
        return user.first().to_entity()

    def compare_password(self, given_password: str, user_password: str) -> bool:
        return check_password(given_password, user_password)

    def update_user(self, user: UserEntity) -> UserEntity:
        User.objects.filter(id=user.id).update(enters_count=user.enters_count)
        return self.get_user_by_id(user.id)

    def create_user(self, user: UserEntity) -> None:
        User.objects.create_user(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,

            email=user.email,
            password=user.password,
            role=user.role,
        )

    def soft_delete_user(self, user: UserEntity) -> None:
        user = User.objects.filter(id=user.id).first()
        if user:
            user.is_deleted = True
            user.deleted_at = timezone.now()
            user.is_active = False
            user.save()


