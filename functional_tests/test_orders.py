import time

from django.contrib.auth import get_user_model

from .base import FunctionalTest
from products.models import Product, Category
from orders.models import Order, Address, Receiver


User = get_user_model()


class OrdersTests(FunctionalTest):

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
        self.address = Address.objects.create(
            city='Москва', street='Манежная', house='2-10',
            apartment='1', postal_code='109012'
        )
        self.receiver = Receiver.objects.create(
            first_name='Ivan', last_name='Ivanov', phone='88005553535'
        )
        self.order = Order.objects.create(
            user=self.user, total_price=self.product.price,
            address=self.address, receiver=self.receiver
        )
        self.order.products.set([self.product])
        self.client.session['cart'] = {
            'products': [str(self.product.pk)],
            'total_sum': float(self.product.price),
        }
        self.client.session.save()
        self._login_user()
        time.sleep(1)

    def _login_user(self):
        self.browser.get(self.live_server_url + '/auth/login/')
        login = self.browser.find_element('css selector', '#id_login')
        password = self.browser.find_element('css selector', '#id_password')
        submit = self.browser.find_element('css selector', '.primaryAction')
        login.send_keys('testuser@gmail.com')
        password.send_keys('testpass')
        submit.click()

    def test_get_all_user_orders(self):
        self.browser.get(self.live_server_url + '/orders/')
        orders = self.browser.find_elements(
            'css selector', '.order'
        )
        self.assertEqual(len(orders), 1)
        order_id = orders[0].find_element(
            'css selector', '.order_id'
        ).text
        self.assertEqual(int(order_id), self.order.pk)
