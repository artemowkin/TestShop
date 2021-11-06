from uuid import UUID

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Category, Product, ProductImage


class CategoryModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='new category')

    def test_created_category_fields(self):
        self.assertEqual(self.category.title, 'new category')

    def test_is_pk_uuid(self):
        self.assertIsInstance(self.category.pk, UUID)

    def test_string_representation(self):
        string_category = str(self.category)
        self.assertEqual(string_category, 'new category')

    def test_is_title_unique(self):
        with self.assertRaises(IntegrityError):
            category_with_existing_title = Category.objects.create(
                title='new category'
            )


class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='new category')
        self.product = Product.objects.create(
            title='new product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )
        self.product_pub_datetime = timezone.now()

    def test_created_product_fields(self):
        self.assertEqual(self.product.title, 'new product')
        self.assertEqual(self.product.price, '500.00')
        self.assertEqual(
            self.product.short_description, 'some short description'
        )
        self.assertEqual(self.product.description, 'some description')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(
            self.product.pub_datetime.date(), self.product_pub_datetime.date()
        )

    def test_is_pk_uuid(self):
        self.assertIsInstance(self.product.pk, UUID)

    def test_string_representation(self):
        string_product = str(self.product)
        self.assertEqual(string_product, 'new product')

    def test_get_absolute_url(self):
        absolute_url = self.product.get_absolute_url()
        self.assertEqual(absolute_url, reverse(
            'concrete_product', args=[str(self.product.pk)]
        ))


class ProductImageModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='new category')
        self.product = Product.objects.create(
            title='new product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )
        ProductImage.objects.create(product=self.product, image='some_image')

    def test_product_images(self):
        product_images = self.product.images.all()
        product_image = product_images[0].image

        self.assertEqual(product_images.count(), 1)
        self.assertEqual(product_image.url, '/media/some_image')

