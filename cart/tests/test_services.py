from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services import Cart
from products.models import Product, Category


User = get_user_model()


class CartTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(title='some category')
        self.product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=self.category
        )
        self.cart = Cart(self.client.session)
        self.client.login(username='testuser', password='testpass')

    def test_get_products(self):
        self.cart.add_product(self.product)
        cart_products = self.cart.get_products()

        self.assertEqual(len(cart_products['products']), 1)
        self.assertEqual(cart_products['products'][0], self.product)
        self.assertEqual(
            float(cart_products['total_sum']), float(self.product.price)
        )
