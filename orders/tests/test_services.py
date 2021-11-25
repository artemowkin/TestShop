from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404

from ..services import GetOrdersService, CreateOrderService
from ..models import Order, Address, Receiver
from products.models import Product, Category


User = get_user_model()


class GetOrdersServiceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
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
        self.service = GetOrdersService(self.user)

    def test_get_all_user_orders_with_logged_in_user(self):
        orders = self.service.get_all()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders[0], self.order)

    def test_get_all_user_orders_with_not_logged_in_user(self):
        with self.assertRaises(PermissionDenied):
            service = GetOrdersService(AnonymousUser())
            service.get_all()

    def test_get_concrete_order_with_logged_in_user(self):
        order = self.service.get_concrete(self.order.pk)
        self.assertEqual(order.pk, self.order.pk)

    def test_get_concrete_order_with_not_logged_in_user(self):
        with self.assertRaises(PermissionDenied):
            service = GetOrdersService(AnonymousUser())
            service.get_concrete(self.order.pk)

    def test_get_concrete_order_with_not_existing_order_pk(self):
        with self.assertRaises(Http404):
            self.service.get_concrete(99999)

    def test_get_concrete_order_with_user_who_is_not_owner_of_order(self):
        new_user = User.objects.create_user(
            username='newuser', password='testpass'
        )
        with self.assertRaises(Http404):
            service = GetOrdersService(new_user)
            service.get_concrete(self.order.pk)


class CreateOrderServiceTests(TestCase):

    def setUp(self):
        self.order_data = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'phone': '88005553535',
            'city': 'Москва',
            'street': 'Манежная',
            'house': '25',
            'apartment': '5',
            'postal_code': '105206'
        }
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(title='test_category')
        self.product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_create_with_logged_in_user(self):
        session = self.client.session
        session['cart'] = {
            'products': [str(self.product.pk)],
            'total_sum': float(self.product.price),
        }
        session.save()
        service = CreateOrderService(self.user, session)
        order = service.create(self.order_data)
        self.assertIsInstance(order.pk, int)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_without_products_in_cart(self):
        session = self.client.session
        service = CreateOrderService(self.user, session)
        with self.assertRaises(PermissionDenied):
            order = service.create(self.order_data)

    def test_create_with_not_logged_in_user(self):
        with self.assertRaises(PermissionDenied):
            service = CreateOrderService(AnonymousUser(), self.client.session)

    def test_create_with_incorrect_phone_number(self):
        self.order_data['phone'] = '123'
        service = CreateOrderService(self.user, self.client.session)
        with self.assertRaises(ValidationError):
            service.create(self.order_data)
