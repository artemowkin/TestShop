from django.urls import path

from . import views


urlpatterns = [
    path(
        'add/<uuid:product_pk>/', views.AddCartProductView.as_view(),
        name='add_product_to_cart'
    ),
]

