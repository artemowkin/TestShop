from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # Local
    path('', include('products.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
]

