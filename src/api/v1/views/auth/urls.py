from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from api.v1.views.auth.handler import (
    RegisterUserView,
    LogoutView,
    ConfirmEmailView,
    AuthMe,
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('confirm_email/', ConfirmEmailView.as_view(), name='confirm'),
    path('me/', AuthMe.as_view(), name='me'),
]