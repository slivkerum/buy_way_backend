import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.entities.products import ProductEntity
from apps.products.entities.characteristics import CharacteristicOptionEntity


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=256, verbose_name=_("Название товара"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    seller_id = models.CharField(max_length=255, verbose_name=_("ID продавца"))
    description = models.TextField(verbose_name=_("Описание"))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', verbose_name=_("Категория"))
    product_characteristics = models.ManyToManyField('CharacteristicOption', related_name='products', verbose_name=_("Выбранные характеристики"))

    def to_entity(self) -> ProductEntity:
        product_characteristics = [
            CharacteristicOptionEntity(id=option.id, title=option.title)
            for option in self.product_characteristics.all()
        ]
        category = self.category.to_entity() if self.category else None
        return ProductEntity(
            id=str(self.id),
            title=self.title,
            amount=float(self.amount),
            description=self.description,
            category=category,
            product_characteristic=product_characteristics
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
