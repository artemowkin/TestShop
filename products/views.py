import logging

from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator

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
        page_obj = self._paginate_reviews(product_reviews)
        product_rating = get_product_rating(product)
        return render(request, 'products/concrete_product.html', {
            'product': product, 'similar_products': similar_products,
            'page_obj': page_obj, 'rating': product_rating
        })

    def _paginate_reviews(self, reviews):
        paginator = Paginator(reviews, 5)
        page_number = self.request.GET.get('page', '')
        if not page_number.isdigit() or page_number == '0':
            page_number = 1
        if int(page_number) > paginator.num_pages:
            page_number = paginator.num_pages

        return paginator.get_page(int(page_number))


class ShopView(View):

    def get(self, request):
        logger.debug(f"Requested GET {request.path} by {request.user}")
        service = ProductsSearchService()
        products = service.search(**request.GET)
        page_obj = self._paginate_products(products)
        return render(request, 'products/shop.html', {'page_obj': page_obj})

    def _paginate_products(self, products):
        paginator = Paginator(products, 3*4)
        page_number = self.request.GET.get('page', '')
        if not page_number.isdigit() or page_number == '0':
            page_number = 1
        if int(page_number) > paginator.num_pages:
            page_number = paginator.num_pages

        return paginator.get_page(int(page_number))
