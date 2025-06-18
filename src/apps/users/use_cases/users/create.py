from dataclasses import dataclass
from typing import Optional
from uuid import uuid4, UUID

from django.db import transaction

from apps.users.entities.organizations import OrganizationEntity
from apps.users.entities.users import UserEntity, UserRole
from apps.users.exceptions.users import UserEmailAlreadyExistsException
from apps.users.services.users import BaseUserService
from apps.users.services.organizations import BaseOrganizationService
from apps.users.use_cases.users.email_confirmation.send import SendEmailConfirmationCodeUseCase


@dataclass
class CreateUserUseCase:
    user_service: BaseUserService
    organization_service: BaseOrganizationService
    email_confirmation_service: SendEmailConfirmationCodeUseCase

    def execute(
            self,
            email: str,
            password: str,
            phone: str,
            first_name: str,
            last_name: str,
            role: UserRole,
            organization: Optional[OrganizationEntity]
    ) -> UserEntity:
        print('s')
        user_entity = UserEntity(
            id=uuid4(),
            email=email,
            password=password,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            role=role,
            organization=organization,
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
            self.email_confirmation_service.execute(user_entity.email)

        return user_entity