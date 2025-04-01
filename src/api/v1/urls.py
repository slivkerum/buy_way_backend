from django.urls import path, include

urlpatterns = [
    path('users/', include('api.v1.views.users.urls')),
    path('', include('api.v1.views.token.urls')),
]