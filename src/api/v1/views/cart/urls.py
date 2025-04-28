from django.urls import path

from api.v1.views.cart.handler import (
    CartView,
    CartProductView,
)

urlpatterns = [
    path('', CartView.as_view(), name='cart-view'),
    path('<uuid:cart_id>/remove/', CartView.as_view(), name='cart-update-delete'),
    path('product/', CartProductView.as_view(), name='cart-product-add'),
    path('product/update/', CartProductView.as_view(), name='cart-product-update'),
    path('product/remove/', CartProductView.as_view(), name='cart-product-remove'),
]
