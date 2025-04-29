from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.entities.categories import CategoryEntity


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_("Название категории"))
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name=_("Родительская категория")
    )
    characteristics = models.ManyToManyField('Characteristic', related_name='categories', verbose_name=_("Характеристики"))

    def to_entity(self) -> CategoryEntity:
        subcategories = [subcategory.to_entity() for subcategory in self.subcategories.all()]
        characteristics = [char.to_entity() for char in self.characteristics.all()]
        return CategoryEntity(
            id=self.id,
            title=self.title,
            parent_category_id=self.parent_category.id if self.parent_category else None,
            subcategories=subcategories,
            characteristics=characteristics
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
