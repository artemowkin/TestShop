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
        self.client.login(username='testuser', password='testpass')
        self.cart = Cart(self.client.session)

    def test_get_products(self):
        category = Category.objects.create(title='some category')
        product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=category
        )
        self.cart.add_product(product)
        cart_products = self.cart.get_products()

        self.assertEqual(len(cart_products['products']), 1)
        self.assertEqual(cart_products['products'][0], product)
        self.assertEqual(
            float(cart_products['total_sum']), float(product.price)
        )

    def test_add_product(self):
        category = Category.objects.create(title='some category')
        product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=category
        )
        self.cart.add_product(product)

        self.assertIn('cart', self.client.session)
        self.assertEqual(
            self.client.session['cart']['products'], [str(product.pk)]
        )

