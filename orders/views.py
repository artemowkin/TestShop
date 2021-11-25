from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError

from cart.services import Cart
from .services import GetOrdersService, CreateOrderService
from .forms import CreateOrderForm


class GetAllOrdersView(View):

	def get(self, request):
		get_service = GetOrdersService(request.user)
		user_orders = get_service.get_all()
		return render(request, 'orders/all_orders.html', {
			'orders': user_orders
		})


class CreateOrderView(View):

	def get(self, request):
		create_order_form = CreateOrderForm()
		return render(request, 'orders/create_order.html', {
			'form': create_order_form
		})

	def post(self, request):
		create_order_form = CreateOrderForm(data=request.POST)
		if create_order_form.is_valid():
			return self.form_valid(create_order_form)

		return self.form_invalid(create_order_form)

	def form_invalid(self, create_order_form):
		return render(self.request, 'orders/create_order.html', {
			'form': create_order_form
		})

	def form_valid(self, create_order_form):
		create_order_service = CreateOrderService(
			self.request.user, self.request.session
		)
		try:
			order = create_order_service.create(create_order_form.cleaned_data)
		except ValidationError as e:
			for field in e.message_dict:
				create_order_form.add_error(field, e.message_dict[field][0])

			return self.form_invalid(create_order_form)

		return redirect(order.get_absolute_url())


class ConcreteOrderView(View):

	def get(self, request, pk):
		get_orders_service = GetOrdersService(request.user)
		order = get_orders_service.get_concrete(pk)
		return render(request, 'orders/concrete.html', {
			'order': order
		})
