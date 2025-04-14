from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from apps.users.models.organizations import Organization
from apps.users.entities.organizations import OrganizationEntity


class BaseOrganizationRepository(ABC):

    @abstractmethod
    def create(self, entity: OrganizationEntity, file) -> OrganizationEntity: ...

    @abstractmethod
    def get_by_owner(self, user_id: UUID) -> list[OrganizationEntity]: ...

    @abstractmethod
    def get_by_id(self, org_id: int) -> OrganizationEntity: ...


class OrganizationRepository(BaseOrganizationRepository):

    def create(self, entity: OrganizationEntity, file) -> OrganizationEntity:
        org = Organization.objects.create(
            name=entity.name,
            owner_id=entity.owner_id,
            documents=file,
            is_active=False
        )
        return org.to_entity()

    def get_by_owner(self, user_id: UUID) -> list[OrganizationEntity]:
        queryset = Organization.objects.filter(owner_id=user_id)
        return [org.to_entity() for org in queryset]

    def get_by_id(self, org_id: int) -> OrganizationEntity:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise Exception(f"Организация с ID {org_id} не найдена")
        return org.to_entity()
