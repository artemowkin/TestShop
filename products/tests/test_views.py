from uuid import uuid4

from django.test import TestCase
from django.urls import reverse

from ..views import HomePageView
from ..models import Product, Category


class HomePageViewTests(TestCase):

    def test_get(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)


class ConcreteProductViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='new category')
        self.product = Product.objects.create(
            title='new product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )

    def test_get(self):
        response = self.client.get(
            reverse('concrete_product', args=[str(self.product.pk)])
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_unexisting_pk(self):
        response = self.client.get(
            reverse('concrete_product', args=[str(uuid4())])
        )
        self.assertEqual(response.status_code, 404)


class ShpoViewTests(TestCase):

    def test_get(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)

