from django.urls import path

from api.v1.views.users.handler import DeleteUserAPIView

urlpatterns = [
    path('delete/', DeleteUserAPIView.as_view(), name='delete-user'),
]