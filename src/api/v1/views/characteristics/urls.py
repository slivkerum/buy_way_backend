from django.urls import path

from api.v1.views.characteristics.handler import (
    CharacteristicListView,
    CharacteristicDetailView,
)

urlpatterns = [
    path('', CharacteristicListView.as_view(), name='characteristic-list'),
    path('<int:characteristic_id>/', CharacteristicDetailView.as_view(), name='characteristic-detail'),
]