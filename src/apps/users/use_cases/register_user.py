from uuid import uuid4
from dataclasses import dataclass

from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import UserEmailAlreadyExistsException
from apps.users.services.users import BaseUserService


@dataclass
class RegisterUserUseCase:
    user_service: BaseUserService

    def execute(self, user_data: dict) -> UserEntity:
        try:
            self.user_service.get_user_by_email(user_data['email'])
            raise UserEmailAlreadyExistsException()
        except UserEmailAlreadyExistsException:
            raise
        except Exception:
            pass

        user_entity = UserEntity(
            id=uuid4(),
            email=user_data["email"],
            password=user_data["password"],
            phone=user_data.get("phone"),
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            role=user_data.get("role"),
        )

        self.user_service.create_user(user_entity)
        return user_entity
