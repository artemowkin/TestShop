from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from products.models import Product, Category


User = get_user_model()


class AddProductToCartViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='some category')
        self.product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=self.category
        )

    def test_post_with_not_logged_in_user(self):
        response = self.client.post(reverse(
            'add_product_to_cart', args=[str(self.product.pk)]
        ))
        self.assertEqual(response.status_code, 403)

    def test_post_with_logged_in_user(self):
        User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse(
            'add_product_to_cart', args=[str(self.product.pk)]
        ))
        self.assertEqual(response.status_code, 201)

