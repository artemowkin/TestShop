from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from products.models import Category, Product
from ..models import Review


User = get_user_model()


class ReviewModelTests(TestCase):

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

    def test_created_review_fields(self):
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.text, 'some review text')

    def test_related_field_name(self):
        self.assertTrue(hasattr(self.product, 'reviews'))
        self.assertEqual(self.product.reviews.all()[0], self.review)

    def test_rating_min_value(self):
        self.review.rating = 0
        with self.assertRaises(ValidationError):
            self.review.full_clean()

    def test_rating_max_value(self):
        self.review.rating = 10
        with self.assertRaises(ValidationError):
            self.review.full_clean()

