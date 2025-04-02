from django.urls import path

from api.v1.views.users.handler import CreateUserAPIView, DeleteUserAPIView

urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='create-user'),
    path('delete/', DeleteUserAPIView.as_view(), name='delete-user'),
]