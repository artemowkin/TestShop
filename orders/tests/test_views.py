from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import Product, Category
from ..models import Order, Address, Receiver


User = get_user_model()


class GetAllOrdersViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_get(self):
        response = self.client.get(reverse('all_orders'))
        self.assertEqual(response.status_code, 200)


class CreateOrderViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_get(self):
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('create_order'))
        self.assertNotEqual(response.status_code, 405)


class ConcreteOrderViewTests(TestCase):

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
        self.client.login(username='testuser', password='testpass')

    def test_get(self):
        response = self.client.get(
            reverse('concrete_order', args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 200)


class DeleteOrderViewTest(TestCase):

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
        self.client.login(username='testuser', password='testpass')

    def test_post(self):
        response = self.client.post(
            reverse('delete_order', args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 302)
