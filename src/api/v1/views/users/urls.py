from django.urls import path

from api.v1.views.users.handler import (
    DeleteUserAPIView,
    OrganizationAPIView,
)

urlpatterns = [
    path('delete/', DeleteUserAPIView.as_view(), name='delete-user'),
    path('organization/file/', OrganizationAPIView.as_view(), name='organization-file'),
]