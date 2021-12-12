import logging

from django.views import View
from django.shortcuts import render

from reviews.services import get_product_reviews
from .services import (
    GetProductsService, get_product_rating, ProductsSearchService
)


logger = logging.getLogger('testshop')


class HomePageView(View):

    def get(self, request):
        logger.debug(f"Requested GET {request.path} by {request.user}")
        service = GetProductsService()
        last_products = service.get_last()
        return render(request, 'products/home.html', {
            'products': last_products
        })


class ConcreteProductView(View):

    def get(self, request, pk):
        logger.debug(f"Requested GET {request.path} by {request.user}")
        service = GetProductsService()
        product = service.get_concrete(pk)
        similar_products = service.get_similar(product)
        product_reviews = get_product_reviews(product)
        product_rating = get_product_rating(product)
        return render(request, 'products/concrete_product.html', {
            'product': product, 'similar_products': similar_products,
            'reviews': product_reviews, 'rating': product_rating
        })


class ShopView(View):

    def get(self, request):
        logger.debug(f"Requested GET {request.path} by {request.user}")
        service = ProductsSearchService()
        products = service.search(**request.GET)
        return render(request, 'products/shop.html', {'products': products})
