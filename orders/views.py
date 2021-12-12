import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from cart.services import Cart
from .services import GetOrdersService, CreateOrderService, delete_order
from .forms import CreateOrderForm


logger = logging.getLogger('testshop')


class GetAllOrdersView(LoginRequiredMixin, View):
	login_url = 'account_login'

	def get(self, request):
		logger.debug(
			f"Requested GET {request.path} by user {request.user.email}"
		)
		get_service = GetOrdersService(request.user)
		user_orders = get_service.get_all()
		return render(request, 'orders/all_orders.html', {
			'orders': user_orders
		})


class CreateOrderView(LoginRequiredMixin, View):
	login_url = 'account_login'

	def get(self, request):
		logger.debug(
			f"Requested GET {request.path} by user {request.user.email}"
		)
		create_order_form = CreateOrderForm()
		cart = Cart(request.session)
		if cart.is_empty():
			logger.warning(f"Requested GET {request.path} with empty cart")
			raise Http404

		return render(request, 'orders/create_order.html', {
			'form': create_order_form
		})

	def post(self, request):
		logger.debug(
			f"Requested POST {request.path} by user {request.user.email}"
		)
		create_order_form = CreateOrderForm(data=request.POST)
		if create_order_form.is_valid():
			return self.form_valid(create_order_form)

		return self.form_invalid(create_order_form)

	def form_invalid(self, create_order_form):
		logger.warning(
			f"Sended incorrect data on {request.path}:"
			f" {create_order_form.errors}"
		)
		return render(self.request, 'orders/create_order.html', {
			'form': create_order_form
		})

	def form_valid(self, create_order_form):
		create_order_service = CreateOrderService(
			self.request.user, self.request.session
		)
		try:
			order = create_order_service.create(create_order_form.cleaned_data)
		except ValidationError:
			return self._handle_validation_error(create_order_form)

		return redirect(order.get_absolute_url())

	def _handle_validation_error(self, create_order_form):
		logger.warning(
			f"{request.path} - Receiver with this phone "
			"number already exists"
		)
		create_order_form.add_error(
			None, 'Receiver with this phone number already exists'
		)
		return self.form_invalid(create_order_form)


class ConcreteOrderView(LoginRequiredMixin, View):
	login_url = 'account_login'

	def get(self, request, pk):
		logger.debug(
			f"Requested GET {request.path} by user {request.user.email}"
		)
		get_orders_service = GetOrdersService(request.user)
		order = get_orders_service.get_concrete(pk)
		return render(self.request, 'orders/concrete.html', {
			'order': order
		})


class DeleteOrderView(LoginRequiredMixin, View):
	login_url = 'account_login'

	def post(self, request, pk):
		logger.debug(
			f"Requested POST {request.path} by user {request.user.email}"
		)
		get_orders_service = GetOrdersService(request.user)
		order = get_orders_service.get_concrete(pk)
		deleted = delete_order(request.user, order)
		if deleted:
			return redirect(reverse('all_orders'))

		return render(self.request, 'orders/concrete.html', {
			'order': order
		})
