import os

from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from django.core.files.uploadedfile import UploadedFile

from apps.users.models.organizations import Organization, OrganizationDocument
from apps.users.models.users import User
from apps.users.entities.organizations import OrganizationEntity
from apps.users.exceptions.organizations import (
    OrganizationNotFound
)


class BaseOrganizationRepository(ABC):

    @abstractmethod
    def create(self, entity: OrganizationEntity, files: list) -> OrganizationEntity: ...

    @abstractmethod
    def get_by_owner(self, user_id: UUID) -> OrganizationEntity: ...

    @abstractmethod
    def get_by_id(self, org_id: int) -> OrganizationEntity: ...

    @abstractmethod
    def remove_file(self, org_id: int, file_id: int) -> None: ...

    @abstractmethod
    def add_file(self, org_id: int, file: UploadedFile) -> None: ...


class OrganizationRepository(BaseOrganizationRepository):

    def create(self, entity: OrganizationEntity, files: list) -> OrganizationEntity:
        owner = User.objects.get(id=entity.owner_id)

        org = Organization.objects.create(
            name=entity.name,
            owner=owner,
            is_active=False
        )

        for file in files:
            OrganizationDocument.objects.create(
                organization=org,
                file=file,
            )

        return org.to_entity()

    def get_by_owner(self, user_id: UUID) -> OrganizationEntity:
        org = Organization.objects.filter(owner_id=user_id).first()
        return org.to_entity()

    def get_by_id(self, org_id: int) -> OrganizationEntity:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise OrganizationNotFound(org_id)
        return org.to_entity()

    def remove_file(self, org_id: int, file_id: int) -> None:
        org = Organization.objects.filter(id=org_id).first()
        if not org:
            raise OrganizationNotFound(org_id)

        document = org.documents.filter(id=file_id).first()
        if document:
            file_path = document.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
            document.delete()

    def add_file(self, org_id: int, file: UploadedFile) -> None:
        org = Organization.objects.filter(id=org_id).first()

        if not org:
            raise OrganizationNotFound(org_id)

        OrganizationDocument.objects.create(
            organization=org,
            file=file,
        )