from django.urls import path, include

urlpatterns = [
    path('', include('api.v1.views.token.urls')),
    path('users/', include('api.v1.views.users.urls')),
    path('auth/', include('api.v1.views.auth.urls')),
    path('products/', include('api.v1.views.products.urls')),
    path('categories/', include('api.v1.views.categories.urls')),
    path('characteristics/', include('api.v1.views.characteristics.urls')),
]