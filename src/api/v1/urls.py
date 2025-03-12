from django.urls import path
from .users.handler import CreateUserAPIView

urlpatterns = [
    path('users/', CreateUserAPIView.as_view(), name='user-create'),
]