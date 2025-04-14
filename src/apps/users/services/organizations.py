from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from apps.users.entities.organizations import OrganizationEntity
from apps.users.repositories.organizations import BaseOrganizationRepository


class BaseOrganizationService(ABC):

    @abstractmethod
    def create_organization(self, entity: OrganizationEntity, file) -> OrganizationEntity: ...

    @abstractmethod
    def get_user_organizations(self, user_id: UUID) -> list[OrganizationEntity]: ...

    @abstractmethod
    def get_by_id(self, org_id: int) -> OrganizationEntity: ...


@dataclass
class OrganizationService(BaseOrganizationService):
    repo: BaseOrganizationRepository

    def create_organization(self, entity: OrganizationEntity, file) -> OrganizationEntity:
        return self.repo.create(entity, file)

    def get_user_organizations(self, user_id: UUID) -> list[OrganizationEntity]:
        return self.repo.get_by_owner(user_id)

    def get_by_id(self, org_id: int) -> OrganizationEntity:
        return self.repo.get_by_id(org_id)
