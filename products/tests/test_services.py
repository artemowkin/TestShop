from uuid import uuid4

from django.test import TestCase
from django.http import Http404
from django.contrib.auth import get_user_model

from reviews.models import Review
from ..services import (
    GetProductsService, get_product_rating, ProductsSearchService
)
from ..models import Category, Product


User = get_user_model()


class GetProductsServiceTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='new category')
        for i in range(1, 52):
            Product.objects.create(
                title=f'new product{i}', price='500.00',
                short_description='some short description',
                description='some description', category=self.category
            )

        self.service = GetProductsService()

    def test_get_last(self):
        last_products = self.service.get_last()
        self.assertEqual(len(last_products), 9)
        self.assertEqual(last_products[0].title, 'new product51')
        self.assertEqual(last_products[-1].title, 'new product43')
        self.assertGreater(
            last_products[1].pub_datetime, last_products[-1].pub_datetime
        )

    def test_get_concrete(self):
        product_pk = Product.objects.first().pk
        product = self.service.get_concrete(product_pk)

        self.assertEqual(product.pk, product_pk)

    def test_get_concrete_with_unexisting_pk(self):
        with self.assertRaises(Http404):
            self.service.get_concrete(uuid4())

    def test_get_similar(self):
        product = Product.objects.first()
        similar_products = self.service.get_similar(product)

        self.assertEqual(len(similar_products), 5)
        self.assertNotIn(product, similar_products)


class GetProductRatingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(title='some category')
        self.product = Product.objects.create(
            title='new product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )
        for i in range(1, 6):
            Review.objects.create(
                user=self.user, product=self.product, rating=i,
                text='some review text'
            )

    def test_get_product_rating(self):
        product_rating = get_product_rating(self.product)
        self.assertEqual(product_rating, 3)

    def test_get_product_rating_with_no_reviews(self):
        self.product.reviews.all().delete()
        product_rating = get_product_rating(self.product)
        self.assertEqual(product_rating, 0)


class ProductsSearchServiceTests(TestCase):

    def setUp(self):
        self.first_category = Category.objects.create(title='first category')
        self.second_category = Category.objects.create(title='second category')
        for i in range(50):
            Product.objects.create(
                title=f'new product ({i})', price=f'{i*5}.00',
                short_description='some short description',
                description='some description', category=self.first_category
            )

        for i in range(50, 100):
            Product.objects.create(
                title=f'new product ({i})', price=f'{i*5}.00',
                short_description='some short description',
                description='some description', category=self.second_category
            )

        self.service = ProductsSearchService()

    def test_search_with_ordering_by_price_to_down(self):
        products = self.service.search(ord_by=['price_down'])

        self.assertEqual(products.count(), 100)
        self.assertGreater(products[0].price, products[1].price)

    def test_search_with_ordering_by_price_to_up(self):
        products = self.service.search(ord_by='price_up')

        self.assertEqual(products.count(), 100)
        self.assertLess(products[0].price, products[1].price)

    def test_search_without_options(self):
        products = self.service.search()

        self.assertEqual(products.count(), 100)

    def test_search_by_category(self):
        products = self.service.search(category=[self.first_category.pk])

        self.assertEqual(products.count(), 50)
        self.assertEqual(products[0].category, self.first_category)

    def test_search_by_max_price(self):
        products = self.service.search(max_price=[500], ord_by=['price_down'])

        self.assertLessEqual(products[0].price, 500)

    def test_search_with_query(self):
        products = self.service.search(query='new product (25)')

        self.assertEqual(products.count(), 1)
        self.assertEqual(products[0].title, 'new product (25)')

