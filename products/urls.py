from django.urls import path

from . import views


urlpatterns = [
    path('home/', views.HomePageView.as_view(), name='homepage'),
    path(
        'shop/<uuid:pk>/', views.ConcreteProductView.as_view(),
        name='concrete_product'
    ),
    path('shop/', views.ShopView.as_view(), name='shop'),
]

