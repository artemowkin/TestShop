from django.shortcuts import render
from django.views import View

from cart.services import Cart
from .services import GetOrdersService


class GetAllOrdersView(View):

	def get(self, request):
		get_service = GetOrdersService(request.user)
		user_orders = get_service.get_all()
		return render(request, 'orders/all_orders.html', {
			'orders': user_orders
		})
