from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path('admin/', admin.site.urls),
]