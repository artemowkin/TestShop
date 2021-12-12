import logging

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

from .services import Cart
from products.services import GetProductsService


logger = logging.getLogger('testshop')


class CartProductsView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        logger.debug(f'Requested GET {request.path} by {request.user.email}')
        cart = Cart(request.session)
        cart_products = cart.get_products()
        return render(request, 'cart/all_products.html', cart_products)

    def post(self, request):
        logger.debug(f'Requested POST {request.path} by {request.user.email}')
        cart = Cart(request.session)
        cart.clear()
        return render(request, 'cart/all_products.html')


class AddCartProductView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def post(self, request, product_pk):
        logger.debug(f'Requested POST {request.path} by {request.user.email}')
        get_products_service = GetProductsService()
        product = get_products_service.get_concrete(product_pk)
        cart = Cart(request.session)
        cart.add_product(product)
        return JsonResponse({'added': True}, status=201)


class RemoveCartProductView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def post(self, request, product_pk):
        logger.debug(f'Requested POST {request.path} by {request.user.email}')
        get_products_service = GetProductsService()
        product = get_products_service.get_concrete(product_pk)
        cart = Cart(request.session)
        cart.remove_product(product)
        return redirect(reverse('cart_all_products'))
