from django.urls import path

from .handler import (
    ReviewDeleteView,
    ReviewDetailView,
    ReviewListCreateView,
)

urlpatterns = [
    path('<uuid:product_id>/', ReviewListCreateView.as_view(), name='review-list-create',),
    path('<int:review_id>/', ReviewDetailView.as_view(), name='review-detail',),
    path('<int:review_id>/delete/', ReviewDeleteView.as_view(), name='review-delete',),
]