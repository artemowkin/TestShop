import re
from uuid import UUID
from typing import Optional, Union
import logging

from django.db.models import QuerySet, Avg, Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import Product


logger = logging.getLogger('testshop')


class GetProductsService:

    def __init__(self) -> None:
        self._model = Product

    def get_last(self) -> list:
        """Return last 9 products ordered by publication date"""
        all_products = self._model.objects.all()
        last_products = all_products.order_by('-pub_datetime')[:9:1]
        logger.debug('Getted last 9 products')
        return last_products

    def get_concrete(self, pk: UUID) -> Product:
        """
        Return a concrete product using pk or raise Http404
        if doesn't exist
        """
        product = get_object_or_404(self._model, pk=pk)
        logger.debug(f'Getted concrete product: {pk}')
        return product

    def get_similar(self, product: Product) -> list:
        """Return 5 similar products in the same category"""
        similar_products = Product.objects.filter(
            category__pk=product.category.pk
        ).exclude(pk=product.pk)[:5:1]
        logger.debug(f'Getted similar products for product {product.pk}')
        return similar_products


class ProductsSearchService:

    def __init__(self):
        self._ordering_fields = {
            'price_down': '-price',
            'price_up': 'price'
        }
        self._model = Product

    def _get_method_queryset(self, kwargs: dict, method_name: str,
            result_queryset: QuerySet) -> QuerySet:
        method = getattr(self, method_name)
        if isinstance(kwargs[method_name], list):
            return method(
                kwargs[method_name], queryset=result_queryset
            )

        return method(
            kwargs[method_name], queryset=result_queryset
        )

    def search(self, **kwargs: dict) -> QuerySet:
        """
        Get search parameters in keyword arguments dict, parse
        it by parameters names, call the method with the same name,
        and return the result queryset
        """
        result_queryset = self._model.objects.all()
        if not self._is_kwargs_valid(kwargs): self._transform_kwargs(kwargs)
        logger.debug(
            f'Requested search products with the following parameters: {kwargs}'
        )
        methods = [
            key for key in kwargs if hasattr(self, key) and kwargs[key]
        ]
        for method_name in methods:
            result_queryset = self._get_method_queryset(
                kwargs, method_name, result_queryset
            )

        return result_queryset

    def _is_kwargs_valid(self, kwargs: dict) -> bool:
        """CHeck is kwargs a dict with list values"""
        return all(
            [not isinstance(kwargs[key], list) for key in kwargs]
        )

    def _transform_kwargs(self, kwargs: dict) -> None:
        """Transform kwargs with values list types"""
        for key in kwargs:
            kwargs[key] = kwargs[key][0]

    def ord_by(self, ordering_type: str,
            queryset: Optional[QuerySet] = None) -> QuerySet:
        """Order queryset by `ordering_type`"""
        ordering_field = self._ordering_fields.get(ordering_type)
        logger.debug(f"Products ordered by {ordering_type}")
        if not ordering_field: return queryset
        if not queryset:
            return self._model.objects.order_by(ordering_field, '-pub_datetime')

        return queryset.order_by(ordering_field, '-pub_datetime')

    def category(self, category_pk: Union[str,UUID],
            queryset: Optional[QuerySet]) -> QuerySet:
        """Search products with concrete category"""
        if not self._is_category_pk_valid(category_pk): return queryset
        logger.debug(f"Products filtered by category: {category_pk}")
        if not queryset:
            return self._model.objects.filter(category__pk=category_pk)

        return queryset.filter(category__pk=category_pk)

    def _is_category_pk_valid(self, category_pk: Union[str,UUID]) -> bool:
        """Check is category pk valid UUID"""
        return re.match(
            r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b",
            str(category_pk)
        )

    def max_price(self, max_price_value: Union[int,str],
            queryset: Optional[QuerySet]) -> QuerySet:
        """Search products with price less or equal max_price_value"""
        if not self._is_max_price_valid(max_price_value): return queryset
        logger.debug(f'Products filtered by max price: {max_price_value}')
        if not queryset:
            return self._model.objects.filter(price__lte=max_price_value)

        return queryset.filter(price__lte=max_price_value)

    def _is_max_price_valid(self, max_price: Union[int,str]) -> bool:
        """Check does max price contain only digits"""
        return re.match(r"\d+", str(max_price))

    def query(self, query_value: str,
            queryset: Optional[QuerySet]) -> QuerySet:
        """Search products using search query"""
        logger.debug(f"Products searched by query: {query_value}")
        if not queryset:
            return self._model.objects.filter(
                Q(title__icontains=query_value) |
                Q(short_description__icontains=query_value)
            )

        return queryset.filter(
            Q(title__icontains=query_value) |
            Q(short_description__icontains=query_value)
        )


def get_product_rating(product: Product) -> float:
    """Return average product rating"""
    all_product_reviews = product.reviews.all()
    product_rating = all_product_reviews.aggregate(
        product_rating=Avg('rating')
    )['product_rating'] or 0.0
    product_rating = round(float(product_rating), 2)
    logger.debug(f"Getted rating ({product_rating}) for product {product.pk}")
    return product_rating or 0.0
