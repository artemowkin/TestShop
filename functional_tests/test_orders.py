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
        self._login_user()
        time.sleep(1)

    def _login_user(self):
        self.browser.get(self.live_server_url + '/auth/login/')
        login = self.browser.find_element('css selector', '#id_login')
        password = self.browser.find_element('css selector', '#id_password')
        submit = self.browser.find_element('css selector', 'button.form_button')
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

    def test_get_all_user_orders(self):
        self.browser.get(self.live_server_url + '/orders/')
        orders = self.browser.find_elements(
            'css selector', '.order'
        )
        self.assertEqual(len(orders), 1)
        order_id = orders[0].find_element(
            'css selector', '.order_id'
        ).text
        self.assertEqual(order_id, f"Order ID: #{self.order.pk}")

    def test_create_a_new_order(self):
        self._add_product_to_cart()
        self.browser.get(self.live_server_url + '/cart/')
        create_order_link = self.browser.find_element(
            'css selector', '.create_order'
        )
        create_order_link.click()
        time.sleep(1)

        # Receiver information
        first_name = self.browser.find_element(
            'css selector', '#id_first_name'
        )
        last_name = self.browser.find_element(
            'css selector', '#id_last_name'
        )
        phone = self.browser.find_element(
            'css selector', '#id_phone'
        )
        first_name.send_keys('Ivan')
        last_name.send_keys('Ivanov')
        phone.send_keys('82225552020')

        # Address information
        city = self.browser.find_element(
            'css selector', '#id_city'
        )
        street = self.browser.find_element(
            'css selector', '#id_street'
        )
        house = self.browser.find_element(
            'css selector', '#id_house'
        )
        apartment = self.browser.find_element(
            'css selector', '#id_apartment'
        )
        postal_code = self.browser.find_element(
            'css selector', '#id_postal_code'
        )
        city.send_keys('Москва')
        street.send_keys('Манежная')
        house.send_keys('25')
        apartment.send_keys('5')
        postal_code.send_keys('105206')
        submit_button = self.browser.find_element(
            'css selector', '#create_order_button'
        )
        submit_button.click()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/orders/')
        time.sleep(1)
        orders = self.browser.find_elements(
            'css selector', '.order'
        )
        self.assertEqual(len(orders), 2)

    def test_create_a_new_order_with_existing_number(self):
        self._add_product_to_cart()
        self.browser.get(self.live_server_url + '/cart/')
        create_order_link = self.browser.find_element(
            'css selector', '.create_order'
        )
        create_order_link.click()
        time.sleep(1)

        # Receiver information
        first_name = self.browser.find_element(
            'css selector', '#id_first_name'
        )
        last_name = self.browser.find_element(
            'css selector', '#id_last_name'
        )
        phone = self.browser.find_element(
            'css selector', '#id_phone'
        )
        first_name.send_keys('Ivan')
        last_name.send_keys('Ivanov')
        phone.send_keys('88005553535')

        # Address information
        city = self.browser.find_element(
            'css selector', '#id_city'
        )
        street = self.browser.find_element(
            'css selector', '#id_street'
        )
        house = self.browser.find_element(
            'css selector', '#id_house'
        )
        apartment = self.browser.find_element(
            'css selector', '#id_apartment'
        )
        postal_code = self.browser.find_element(
            'css selector', '#id_postal_code'
        )
        city.send_keys('Москва')
        street.send_keys('Манежная')
        house.send_keys('25')
        apartment.send_keys('5')
        postal_code.send_keys('105206')
        submit_button = self.browser.find_element(
            'css selector', '#create_order_button'
        )
        submit_button.click()
        time.sleep(1)
        errorlist = self.browser.find_element('css selector', '.errorlist')
        self.assertTrue(errorlist)

    def test_cart_page_has_no_create_order_link_if_cart_is_empty(self):
        self.browser.get(self.live_server_url + '/cart/')
        create_order_link = self.browser.find_elements(
            'css selector', '.create_order'
        )
        self.assertEqual(len(create_order_link), 0)

    def test_get_concrete_order(self):
        self._add_product_to_cart()
        self.browser.get(self.live_server_url + f"/orders/{self.order.pk}/")
        order_id = self.browser.find_element(
            'css selector', '.order_id'
        ).text
        self.assertEqual(order_id, str(self.order.pk))


    def test_delete_a_concrete_order(self):
        self._add_product_to_cart()
        self.browser.get(self.live_server_url + f"/orders/{self.order.pk}/")
        delete_order_button = self.browser.find_element(
            'css selector', '.delete_order'
        )
        delete_order_button.click()
        time.sleep(1)
        orders = self.browser.find_elements(
            'css selector', '.order'
        )
        self.assertEqual(len(orders), 0)

    def test_delete_a_concrete_order_with_sent_status(self):
        self.order.status = 'sent'
        self.order.save()
        self._add_product_to_cart()
        self.browser.get(self.live_server_url + f"/orders/{self.order.pk}/")
        delete_order_buttons = self.browser.find_elements(
            'css selector', '.delete_order'
        )
        self.assertEqual(len(delete_order_buttons), 0)
