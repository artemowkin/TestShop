from uuid import UUID
from typing import Optional, Union

from django.db.models import QuerySet, Avg, Q
from django.shortcuts import get_object_or_404

from .models import Product


class GetProductsService:

    def __init__(self) -> None:
        self._model = Product

    def get_last(self) -> list:
        """Return last 50 products ordered by publication date"""
        all_products = self._model.objects.all()
        last_products = all_products.order_by('-pub_datetime')[:50:1]
        return last_products

    def get_concrete(self, pk: UUID) -> Product:
        """
        Return a concrete product using pk or raise Http404
        if doesn't exist
        """
        product = get_object_or_404(self._model, pk=pk)
        return product

    def get_similar(self, product: Product) -> list:
        """Return 5 similar products in the same category"""
        similar_products = Product.objects.filter(
            category__pk=product.category.pk
        ).exclude(pk=product.pk)[:5:1]
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
                kwargs[method_name][0], queryset=result_queryset
            )

        return method(
            kwargs[method_name], queryset=result_queryset
        )

    def search(self, **kwargs) -> QuerySet:
        """
        Get search parameters in keyword arguments dict, parse
        it by parameters names, call the method with the same name,
        and return the result queryset
        """
        result_queryset = self._model.objects.all()
        methods = [key for key in kwargs if hasattr(self, key)]
        for method_name in methods:
            result_queryset = self._get_method_queryset(
                kwargs, method_name, result_queryset
            )

        return result_queryset

    def ord_by(self, ordering_type: str,
            queryset: Optional[QuerySet] = None) -> QuerySet:
        """Order queryset by `ordering_type`"""
        ordering_field = self._ordering_fields[ordering_type]
        if not queryset:
            return self._model.objects.order_by(ordering_field)

        return queryset.order_by(ordering_field)

    def category(self, category_pk: Union[str,UUID],
            queryset: Optional[QuerySet]) -> QuerySet:
        """Search products with concrete category"""
        if not queryset:
            return self._model.objects.filter(category__pk=category_pk)

        return queryset.filter(category__pk=category_pk)

    def max_price(self, max_price_value: int,
            queryset: Optional[QuerySet]) -> QuerySet:
        """Search products with price less or equal max_price_value"""
        if not queryset:
            return self._model.objects.filter(price__lte=max_price_value)

        return queryset.filter(price__lte=max_price_value)

    def query(self, query_value: str,
            queryset: Optional[QuerySet]) -> QuerySet:
        """Search products using search query"""
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
    )['product_rating']
    return product_rating or 0.0

