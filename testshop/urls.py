from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


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

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
