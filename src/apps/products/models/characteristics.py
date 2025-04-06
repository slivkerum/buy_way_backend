from django.db import models
from django.utils.translation import gettext_lazy as _  # Для локализации

from apps.products.entities.characteristics import (
    CharacteristicOptionEntity,
    CharacteristicEntity,
)


class Characteristic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_("Название характеристики"))

    def to_entity(self) -> CharacteristicEntity:
        options = [option.to_entity() for option in self.options.all()]
        return CharacteristicEntity(
            id=self.id,
            title=self.title,
            options=options
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Характеристика")
        verbose_name_plural = _("Характеристики")


class CharacteristicOption(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, verbose_name=_("Значение характеристики"))
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE, related_name='options', verbose_name=_("Характеристика"))

    def to_entity(self) -> CharacteristicOptionEntity:
        return CharacteristicOptionEntity(
            id=self.id,
            title=self.title
        )

    def __str__(self):
        return f"{self.characteristic.title}: {self.title}"

    class Meta:
        verbose_name = _("Значение характеристики")
        verbose_name_plural = _("Значения характеристик")
