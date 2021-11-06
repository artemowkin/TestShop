from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ValidationError

from products.models import Category, Product
from ..models import Review
from ..services import get_product_reviews, CreateReviewService


User = get_user_model()


class GetProductReviewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(title='some category')
        self.product = Product.objects.create(
            title='new product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )
        self.review = Review.objects.create(
            user=self.user, product=self.product, rating=5,
            text='some review text'
        )

    def test_get_product_reviews_return_product_reviews(self):
        product_reviews = get_product_reviews(self.product)

        self.assertEqual(product_reviews.count(), 1)
        self.assertEqual(product_reviews[0], self.review)


class CreateReviewServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(title='some category')
        self.product = Product.objects.create(
            title='new product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )
        self.service = CreateReviewService()

    def test_create(self):
        review = self.service.create(
            self.product.pk, self.user.pk, 5, 'some review'
        )

        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, 'some review')

    def test_create_with_incorrect_rating(self):
        with self.assertRaises(ValidationError):
            review = self.service.create(
                self.product.pk, self.user.pk, 10, 'some review'
            )

