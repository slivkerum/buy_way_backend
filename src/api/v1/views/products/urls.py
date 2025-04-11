from django.urls import path

from api.v1.views.products.handler import (
    ProductListCreateView,
    ProductDetailView,
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('<uuid:product_id>/', ProductDetailView.as_view(), name='product-detail'),
]