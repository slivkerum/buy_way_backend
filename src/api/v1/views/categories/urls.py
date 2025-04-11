from django.urls import path
from api.v1.views.categories.handler import (
    CategoryListView,
    CategoryDetailView
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
]