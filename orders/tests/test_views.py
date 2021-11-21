from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


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
