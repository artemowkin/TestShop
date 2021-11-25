from django.urls import path

from . import views


urlpatterns = [
	path('', views.GetAllOrdersView.as_view(), name='all_orders'),
	path('create/', views.CreateOrderView.as_view(), name='create_order'),
	path(
		'<int:pk>/', views.ConcreteOrderView.as_view(),
		name='concrete_order'
	),
]
