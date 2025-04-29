import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.users.entities.organizations import (
    OrganizationEntity
)


def organization_documents_upload_path(instance, filename):
    return f"organizations/{instance.organization.owner_id}/{filename}"


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_("Название организации"))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organizations",
        verbose_name=_("Владелец")
    )
    is_active = models.BooleanField(default=False, verbose_name=_("Активна"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (owner: {self.owner})"

    class Meta:
        verbose_name = _("Организация")
        verbose_name_plural = _("Организации")

    def to_entity(self) -> OrganizationEntity:
        documents_paths = [doc.file.url for doc in self.documents.all()]
        return OrganizationEntity(
            id=self.id,
            name=self.name,
            owner_id=self.owner.id,
            created_at=self.created_at,
            documents_path=documents_paths,
            is_active=self.is_active
        )


class OrganizationDocument(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Организация")
    )
    file = models.FileField(
        upload_to=organization_documents_upload_path,
        verbose_name=_("Документ (PDF)")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Документ организации {self.organization.name} (ID: {self.id})"

    class Meta:
        verbose_name = _("Документ организации")
        verbose_name_plural = _("Документы организаций")

