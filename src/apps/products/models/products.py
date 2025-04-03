import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Characteristic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_("Название характеристики"))

    class Meta:
        verbose_name = _("Характеристика")
        verbose_name_plural = _("Характеристики")

    def __str__(self):
        return self.title


class CharacteristicOption(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, verbose_name=_('Значение характеристики'))
    characteristic = models.ForeignKey(
        Characteristic,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('Характеристика')
    )

    class Meta:
        verbose_name = _("Опция характеристики")
        verbose_name_plural = _("Опции характеристик")

    def __str__(self):
        return f'{self.characteristic.title}: {self.title}'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256, verbose_name=_("Название товара"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    description = models.TextField(verbose_name=_("Описание"))
    characteristic = models.ManyToManyField(
        CharacteristicOption,
        related_name='products',
        verbose_name=_("Выбранные характеристики"),
    )

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.title