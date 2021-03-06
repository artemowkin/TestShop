import logging

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import Review
from products.models import Product
from products.services import GetProductsService


User = get_user_model()
logger = logging.getLogger('testshop')


def get_product_reviews(product: Product) -> QuerySet:
    """Return all product reviews"""
    product_reviews = product.reviews.all()
    logger.debug(f"Getted all reviews for product {product.pk}")
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
        self._handle_not_authenticated_user(user, product_pk)
        product = self._get_products_service.get_concrete(product_pk)
        return self._create_review_entry(product, user, rating, text)

    def _create_review_entry(self, product: Product, user: User,
            rating: int, text: str) -> Review:
        """Create the review model entry"""
        review = self._model(
            product=product, user=user, rating=rating, text=text
        )
        review.full_clean()
        review.save()
        logger.debug(
            f"Created a new review for product {product.pk} "
            f"by user {user.email}"
        )
        return review

    def _handle_not_authenticated_user(self, user: User,
            product_pk: str) -> None:
        """Handle if user is not authenticated"""
        if not user.is_authenticated:
            logger.warning(
                f"Creating a new review for product {product_pk} by "
                "not authenticated user"
            )
            raise PermissionDenied
