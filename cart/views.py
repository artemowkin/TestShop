from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse

from .services import Cart
from products.services import GetProductsService


class AddCartProductView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request, product_pk):
        get_products_service = GetProductsService()
        product = get_products_service.get_concrete(product_pk)
        cart = Cart(request.session)
        cart.add_product(product)
        return JsonResponse({'added': True}, status=201)

