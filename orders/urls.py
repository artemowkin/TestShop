from django.urls import path

from . import views


urlpatterns = [
	path('', views.GetAllOrdersView.as_view(), name='all_orders'),
]
