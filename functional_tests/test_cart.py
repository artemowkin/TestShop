import time

from django.contrib.auth import get_user_model

from .base import FunctionalTest
from products.models import Product, Category


User = get_user_model()


class ConcreteProductTests(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass',
            email='testuser@gmail.com'
        )
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(title='test_category')
        self.product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=self.category
        )
        self.client.session['cart'] = {
            'products': [str(self.product.pk)],
            'total_sum': float(self.product.price),
        }
        self.client.session.save()
        self._login_user()
        time.sleep(1)
        self._add_product_to_cart()
        self.browser.get(self.live_server_url + '/cart/')

    def _login_user(self):
        self.browser.get(self.live_server_url + '/auth/login/')
        login = self.browser.find_element('css selector', '#id_login')
        password = self.browser.find_element('css selector', '#id_password')
        submit = self.browser.find_element('css selector', '.primaryAction')
        login.send_keys('testuser@gmail.com')
        password.send_keys('testpass')
        submit.click()

    def _add_product_to_cart(self):
        self.browser.get(self.live_server_url + f'/shop/{self.product.pk}/')
        add_button = self.browser.find_element(
            'css selector', '.product_add_to_cart'
        )
        add_button.click()
        time.sleep(1)

    def test_get_all_cart_products(self):
        cart_products = self.browser.find_elements(
            'css selector', '.product'
        )
        self.assertEqual(len(cart_products), 1)
        cart_product_title = cart_products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(cart_product_title, self.product.title)
        total_sum = self.browser.find_element(
            'css selector', '.products_total_sum'
        ).text
        self.assertEqual(float(total_sum), float(self.product.price))

    def test_clear(self):
        clear_button = self.browser.find_element(
            'css selector', '.clear_cart_button'
        )
        self.assertTrue(clear_button)
        clear_button.click()
        time.sleep(1)
        products = self.browser.find_elements(
            'css selector', '.product'
        )
        self.assertEqual(len(products), 0)

    def test_remove(self):
        self.browser.get(self.live_server_url + '/cart/')
        remove_button = self.browser.find_element(
            'css selector', '.remove_product'
        )
        remove_button.click()
        time.sleep(1)
        products = self.browser.find_elements(
            'css selector', '.product'
        )
        self.assertEqual(len(products), 0)

