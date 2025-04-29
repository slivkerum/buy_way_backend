from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.products.entities.reviews import ReviewEntity


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Пользователь")
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Товар")
    )
    rating = models.PositiveSmallIntegerField(verbose_name=_("Оценка (1–5)"))
    text = models.TextField(verbose_name=_("Текст отзыва"))
    created_at = models.DateTimeField(default=now, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(default=now, verbose_name=_("Обновлён"))

    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            id=self.id,
            user_id=self.user.id,
            product_id=self.product.id,
            rating=self.rating,
            text=self.text,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self):
        return _("Отзыв на {product} от {user}").format(
            product=self.product.title, user=self.user.email
        )
