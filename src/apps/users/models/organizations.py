import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.common.models import BaseDateTimeModel
from apps.users.entities.organizations import (
    OrganizationEntity,
    OrganizationDocumentsEntity,
)


def organization_documents_upload_path(instance, filename):
    return f"organizations/{instance.organization.name}/{filename}"


class Organization(BaseDateTimeModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_("Название организации"))

    is_active = models.BooleanField(default=False, verbose_name=_("Активна"))

    def to_entity(self) -> OrganizationEntity:
        return OrganizationEntity(
            id=self.id,
            name=self.name,
            is_active=self.is_active,
            documents=[
                document.to_entity() for document in self.documents.all()
            ],
        )

    @classmethod
    def from_entity(cls, organization: OrganizationEntity):
        return cls(
            name=organization.name,
            is_active=organization.is_active
        )

    def __str__(self):
        return f"{self.name})"

    class Meta:
        verbose_name = _("Организация")
        verbose_name_plural = _("Организации")


class OrganizationDocuments(BaseDateTimeModel):
    name = models.CharField(max_length=255, verbose_name=_("Название документа"))
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Организация"),
    )

    path = models.FileField(upload_to=organization_documents_upload_path)

    def to_entity(self) -> OrganizationDocumentsEntity:
        return OrganizationDocumentsEntity(
            id=self.id,
            name=self.name,
            path=self.path.path,
        )

    @classmethod
    def from_entity(cls, documents: OrganizationDocumentsEntity, organization: Organization):
        return cls(
            name=documents.name,
            path=documents.path,
            organization=organization,
        )

    def __str__(self):
        return f'{self.name}(path: {self.path})'

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")
