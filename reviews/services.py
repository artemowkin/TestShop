from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import Review
from products.models import Product
from products.services import GetProductsService


User = get_user_model()


def get_product_reviews(product: Product) -> QuerySet:
    """Return all product reviews"""
    product_reviews = product.reviews.all()
    return product_reviews


class CreateReviewService:
    """Service to create a new review for the existing product"""

    def __init__(self):
        self._get_products_service = GetProductsService()
        self._model = Review

    def create(self, product_pk: str, user: User,
            rating: int, text: str) -> Review:
        """
        Create a new review for product from user (if authenticated)
        with rating and text
        """
        if not user.is_authenticated: raise PermissionDenied
        product = self._get_products_service.get_concrete(product_pk)
        review = self._model(
            product=product, user=user, rating=rating, text=text
        )
        review.full_clean()
        review.save()
        return review

