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
        session = self.client.session
        self.cart = Cart(session)
        self.client.login(username='testuser', password='testpass')

    def test_get_products_and_add_product(self):
        self.cart.add_product(self.product)
        cart_products = self.cart.get_products()

        self.assertEqual(len(cart_products['products']), 1)
        self.assertEqual(cart_products['products'][0], self.product)
        self.assertEqual(
            float(cart_products['total_sum']), float(self.product.price)
        )

    def test_clear(self):
        self.cart.add_product(self.product)
        self.cart.clear()
        cart_products = self.cart.get_products()

        self.assertEqual(len(cart_products['products']), 0)
        self.assertEqual(cart_products['total_sum'], 0.0)

    def test_remove_product(self):
        self.cart.add_product(self.product)
        self.cart.remove_product(self.product)
        cart_products = self.cart.get_products()

        self.assertEqual(len(cart_products['products']), 0)
        self.assertEqual(cart_products['total_sum'], 0.0)

    def test_is_empty(self):
        self.assertTrue(self.cart.is_empty())
        self.cart.add_product(self.product)
        self.assertFalse(self.cart.is_empty())

    def test_has_product_with_empty_cart(self):
        self.assertFalse(self.cart.has_product(self.product))

    def test_has_product_with_product_in_cart(self):
        self.cart.add_product(self.product)
        self.assertTrue(self.cart.has_product(self.product))
