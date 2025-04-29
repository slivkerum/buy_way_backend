from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from api.v1.views.auth.handler import (
    RegisterUserView,
    LogoutView
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
]