from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('auth/', include('allauth.urls')),

    # Local
    path('', include('products.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]
