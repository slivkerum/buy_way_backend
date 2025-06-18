from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.core.files.base import ContentFile
from ninja import UploadedFile

from apps.users.entities.organizations import OrganizationEntity, OrganizationDocumentsEntity
from apps.users.exceptions.organizations import OrganizationNotFoundException
from apps.users.models.organizations import Organization, OrganizationDocuments
from apps.users.repositories.organizations import BaseOrganizationRepository


class BaseOrganizationService(ABC):

    @abstractmethod
    def get_by_id(self, org_id: int) -> OrganizationEntity: ...

    @abstractmethod
    def update_fields(self, org_id: int, **kwargs) -> None: ...

    @abstractmethod
    def create_organization(self, organization: OrganizationEntity) -> OrganizationEntity: ...

    @abstractmethod
    def add_documents(self, org_id: int, document: OrganizationDocumentsEntity, file: UploadedFile) -> None: ...

    @abstractmethod
    def remove_documents(self, org_id: int, document_id: int) -> None: ...


@dataclass
class OrganizationService(BaseOrganizationService):
    repo: BaseOrganizationRepository

    def get_by_id(self, org_id: int) -> OrganizationEntity:
        return self.repo.get_by_id(org_id)

    def update_fields(self, org_id: int, **kwargs) -> None:
        self.repo.update_fields(org_id, **kwargs)

    def create_organization(self, organization: OrganizationEntity) -> OrganizationEntity:
        return self.repo.create_organization(organization)

    def add_documents(self, org_id: int, document: OrganizationDocumentsEntity, file: UploadedFile) -> None:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise OrganizationNotFoundException(org_id)

        document_model = OrganizationDocuments(
            name=document.name,
            organization=org
        )
        document_model.path.save(file.name, ContentFile(file.read()))
        document_model.save()

    def remove_documents(self, org_id: int, document_id: int) -> None:
        self.repo.remove_document(org_id, document_id)
