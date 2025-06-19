from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.products.entities.cart import (
    CartEntity,
    CartProductEntity,
)


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('Пользователь')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Цена всех товаров')
    )

    def to_entity(self) -> 'CartEntity':
        return CartEntity(
            id=self.id,
            user_id=self.user_id,
            total_price=self.total_price,
            created_at=self.created_at,
            items=[item.to_entity() for item in self.items.all()]
        )

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Корзина')
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name=_('Товар')
    )
    quantity = models.IntegerField(default=0, verbose_name=_('Количество'))

    def to_entity(self) -> 'CartProductEntity':
        return CartProductEntity(
            id=self.id,
            product_id=self.product_id,
            quantity=self.quantity
        )

    class Meta:
        verbose_name = _('Товар в корзине')
        verbose_name_plural = _('Товары в корзинах')
