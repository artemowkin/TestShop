from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from ..services import GetOrdersService
from ..models import Order, Address, Receiver
from products.models import Product, Category


User = get_user_model()


class GetProductsServiceTests(TestCase):

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
