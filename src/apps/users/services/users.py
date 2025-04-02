from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from uuid import UUID

from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import UserIdNotFound
from apps.users.repositories.users import BaseUserRepository


class BaseUserService(ABC):

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
    def soft_delete_user(self, user_id: UUID) -> bool:...


@dataclass
class UserService(BaseUserService):
    user_repository: BaseUserRepository

    def get_user_by_id(self, user_id: UUID) -> UserEntity:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> UserEntity:
        return self.user_repository.get_user_by_email(email)

    def compare_password(self, given_password: str, user_password: str) -> bool:
        return self.user_repository.compare_password(given_password=given_password, user_password=user_password)

    def update_user(self, user: UserEntity) -> UserEntity:
        return self.user_repository.update_user(user)

    def create_user(self, user: UserEntity) -> None:
        self.user_repository.create_user(user)

    def soft_delete_user(self, user_id: UUID) -> bool:
        try:
            user = self.user_repository.get_user_by_id(user_id)
        except UserIdNotFound:
            return False

        self.user_repository.soft_delete_user(user)
        return True

