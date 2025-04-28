from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from django.core.files.uploadedfile import UploadedFile

from apps.users.entities.organizations import OrganizationEntity
from apps.users.repositories.organizations import BaseOrganizationRepository


class BaseOrganizationService(ABC):

    @abstractmethod
    def create_organization(self, entity: OrganizationEntity, files: list) -> OrganizationEntity: ...

    @abstractmethod
    def get_user_organizations(self, user_id: UUID) -> OrganizationEntity: ...

    @abstractmethod
    def get_by_id(self, org_id: int) -> OrganizationEntity: ...

    @abstractmethod
    def remove_file(self, org_id: int, file_id: int) -> None: ...

    @abstractmethod
    def add_file(self, org_id: int, file: UploadedFile) -> None: ...


@dataclass
class OrganizationService(BaseOrganizationService):
    repo: BaseOrganizationRepository

    def create_organization(self, entity: OrganizationEntity, files: list) -> OrganizationEntity:
        return self.repo.create(entity, files)

    def get_user_organizations(self, user_id: UUID) -> OrganizationEntity:
        return self.repo.get_by_owner(user_id)

    def get_by_id(self, org_id: int) -> OrganizationEntity:
        return self.repo.get_by_id(org_id)

    def remove_file(self, org_id: int, file_id: int) -> None:
        self.repo.remove_file(org_id, file_id)

    def add_file(self, org_id: int, file: UploadedFile) -> None:
        self.repo.add_file(org_id, file)
