from abc import ABC, abstractmethod
from uuid import UUID

from django.contrib.auth.hashers import check_password
from django.db.models import Q

from apps.users.filters.users import UserFilters
from apps.users.models.users import User
from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import (
    UserIdNotFound,
    UserEmailNotFound,
)


class BaseUserRepository(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> UserEntity: ...

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity: ...

    @abstractmethod
    def compare_passwords(self, given_password: str, user_password: str) -> bool: ...

    @abstractmethod
    def update_user(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity: ...


class UserRepository(BaseUserRepository):

    def get_user_by_id(self, user_id: UUID) -> UserEntity:
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise UserIdNotFound(user_id)
        return user.to_entity()

    def get_user_by_email(self, email: str) -> UserEntity:
        user = User.objects.filter(email=email).first()
        if not user:
            raise UserEmailNotFound(email)
        return user.to_entity()

    def compare_passwords(self, given_password: str, user_password: str) -> bool:
        return check_password(given_password, user_password)

    def update_user(self, user: UserEntity) -> UserEntity:
        User.objects.filter(id=user.id).update(
            enters_count=user.enters_count
        )
        return self.get_user_by_id(user.id)

    def create_user(self, user: UserEntity) -> UserEntity:
        user_model = User.from_entity(user)
        user_model.set_password(user.password)
        user_model.save()
        return user_model.to_entity()