from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..models import Order, Receiver, Address
from products.models import Product, Category


User = get_user_model()


class ReceiverModelTests(TestCase):

    def setUp(self):
        self.receiver = Receiver.objects.create(
            first_name='Ivan', last_name='Ivanov', phone='88005553535'
        )

    def test_created_entry_fields(self):
        self.assertIsInstance(self.receiver.pk, int)
        self.assertEqual(self.receiver.first_name, 'Ivan')
        self.assertEqual(self.receiver.last_name, 'Ivanov')
        self.assertEqual(self.receiver.phone, '88005553535')

    def test_check_does_invalid_number_raise_exception(self):
        with self.assertRaises(ValidationError):
            receiver = Receiver.objects.create(
                first_name='Ivan', last_name='Ivanov', phone='123'
            )
            receiver.full_clean()


class AddressModelTests(TestCase):

    def setUp(self):
        self.address = Address.objects.create(
            city='Москва', street='Манежная', house='2-10',
            apartment='1', postal_code='109012'
        )

    def test_created_entry_fields(self):
        self.assertIsInstance(self.address.pk, int)
        self.assertEqual(self.address.city, 'Москва')
        self.assertEqual(self.address.street, 'Манежная')
        self.assertEqual(self.address.house, '2-10')
        self.assertEqual(self.address.apartment, '1')
        self.assertEqual(self.address.postal_code, '109012')

    def test_check_does_invalid_postal_code_raise_exception(self):
        with self.assertRaises(ValidationError):
            address = Address.objects.create(
                city='Москва', street='Манежная', house='2-10',
                postal_code='123'
            )
            address.full_clean()


class OrderModelTests(TestCase):

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
        self.order.products.set([self.product])

    def test_created_order_fields(self):
        self.assertIsInstance(self.order.pk, int)
        self.assertEqual(self.order.products.count(), 1)
        self.assertEqual(self.order.products.all()[0], self.product)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, 'processing')
        self.assertEqual(self.order.total_price, self.product.price)
        self.assertEqual(self.order.address, self.address)
        self.assertEqual(self.order.receiver, self.receiver)

