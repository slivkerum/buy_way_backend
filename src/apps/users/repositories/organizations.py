import os
from abc import (
    ABC,
    abstractmethod,
)


from apps.users.models.organizations import Organization, OrganizationDocuments
from apps.users.entities.organizations import OrganizationEntity, OrganizationDocumentsEntity
from apps.users.exceptions.organizations import (
    OrganizationNotFoundException
)


class BaseOrganizationRepository(ABC):

    @abstractmethod
    def get_by_id(self, org_id: int) -> OrganizationEntity: ...

    @abstractmethod
    def update_fields(self, org_id: int, **kwargs) -> None: ...

    @abstractmethod
    def create_organization(self, organization: OrganizationEntity) -> OrganizationEntity: ...

    @abstractmethod
    def add_document(self, org_id: int, document_id: OrganizationDocumentsEntity) -> None: ...

    @abstractmethod
    def remove_document(self, org_id: int, document_id: int) -> None: ...


class OrganizationRepository(BaseOrganizationRepository):

    def get_by_id(self, org_id: int) -> OrganizationEntity:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise OrganizationNotFoundException(org_id)
        return org.to_entity()

    def update_fields(self, org_id: int, **kwargs) -> None:
        org = Organization.objects.filter(id=org_id)
        if not org:
            raise OrganizationNotFoundException(org_id)
        org.update(**kwargs)

    def create_organization(self, organization: OrganizationEntity) -> OrganizationEntity:
        organization_model = Organization.from_entity(organization)
        organization_model.save()
        return organization_model.to_entity()

    def add_document(self, org_id: int, document: OrganizationDocumentsEntity) -> None:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise OrganizationNotFoundException(org_id)

        document_model = OrganizationDocuments.from_entity(document, organization=org)
        document_model.save()

    def remove_document(self, org_id: int, document_id: int) -> None:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise OrganizationNotFoundException(org_id)

        document = org.documents.filter(id=document_id).first()
        if document:
            file_path = document.path.path
            if os.path.exists(file_path):
                os.remove(file_path)
            document.delete()