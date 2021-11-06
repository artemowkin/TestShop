from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from products.models import Product, Category


User = get_user_model()


class AddProductReviewViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(title='some category')
        self.product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=self.category
        )

    def test_get(self):
        response = self.client.get(reverse(
            'add_product_review', args=[str(self.product.pk)]
        ))
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        response = self.client.post(
            reverse('add_product_review', args=[str(self.product.pk)]), {
            'user': self.user.pk, 'product': str(self.product.pk),
            'rating': 5, 'text': 'some review'
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_post_with_not_json_data(self):
        response = self.client.post(
            reverse('add_product_review', args=[str(self.product.pk)])
        )
        self.assertEqual(response.status_code, 404)

