from dataclasses import dataclass
from uuid import uuid4

from django.db import transaction

from apps.users.entities.users import UserEntity
from apps.users.exceptions.users import UserEmailAlreadyExistsException
from apps.users.services.users import BaseUserService
from apps.users.services.organizations import BaseOrganizationService
from apps.users.use_cases.users.email_confirmation.send import SendEmailConfirmationCodeUseCase


@dataclass
class CreateUserUseCase:
    user_service: BaseUserService
    organization_service: BaseOrganizationService
    email_confirmation_service: SendEmailConfirmationCodeUseCase

    def execute(self, user_data: dict) -> UserEntity:
        user_entity = UserEntity(
            id=uuid4(),
            email=user_data["email"],
            password=user_data["password"],
            phone=user_data.get("phone"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            role=user_data.get("role"),
            is_active=user_data.get("is_active", False),
            organization=user_data.get("organization"),
        )

        try:
            user = self.user_service.get_user_by_email(user_entity.email)
            if not user.is_active:
                self.email_confirmation_service.execute(user_entity.email)
                return user
            raise UserEmailAlreadyExistsException()
        except UserEmailAlreadyExistsException:
            raise
        except Exception:
            pass

        with transaction.atomic():
            self.user_service.create_user(user_entity)
            self.user_service.update_user(user_entity)
            self.email_confirmation_service.execute(user_entity.email)

        return user_entity