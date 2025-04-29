from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass

from django.db import transaction

from apps.users.entities.users import UserEntity
from apps.users.entities.organizations import OrganizationEntity
from apps.users.exceptions.users import UserEmailAlreadyExistsException
from apps.users.services.users import BaseUserService
from apps.users.services.organizations import BaseOrganizationService
from apps.users.entities.users import UserRole


@dataclass
class RegisterUserUseCase:
    organization_service: BaseOrganizationService
    user_service: BaseUserService

    def execute(self, user_data: dict, files=None) -> UserEntity:
        try:
            self.user_service.get_user_by_email(user_data['email'])
            raise UserEmailAlreadyExistsException()
        except UserEmailAlreadyExistsException:
            raise
        except Exception:
            pass

        with transaction.atomic():
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

            if user_entity.role == UserRole.SELLER.value:
                organization_entity = OrganizationEntity(
                    id=0,
                    name=user_data["organization_name"],
                    owner_id=user_entity.id,
                    created_at=datetime.utcnow(),
                    documents_path=[],
                    is_active=False
                )
                self.organization_service.create_organization(
                    organization_entity,
                    files.getlist("organization_documents")
                )

        return user_entity
