from django.urls import path, include

urlpatterns = [
    path('products/reviews/', include('api.v1.views.reviews.urls')),
    path('products/', include('api.v1.views.products.urls')),
    path('users/', include('api.v1.views.users.urls')),
    path('auth/', include('api.v1.views.auth.urls')),
    path('categories/', include('api.v1.views.categories.urls')),
    path('characteristics/', include('api.v1.views.characteristics.urls')),
    path('', include('api.v1.views.token.urls')),
]