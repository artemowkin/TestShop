from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartProductsView.as_view(), name='cart_all_products'),
    path(
        'add/<uuid:product_pk>/', views.AddCartProductView.as_view(),
        name='add_product_to_cart'
    ),
    path(
        'remove/<uuid:product_pk>/', views.RemoveCartProductView.as_view(),
        name='remove_cart_product'
    )
]

