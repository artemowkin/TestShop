from django.test import TestCase

from ..forms import CreateOrderForm


class CreateOrderFormTests(TestCase):

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

    def test_form_fields(self):
        form = CreateOrderForm()
        self.assertEqual(form.fields.keys(), self.order_data.keys())

    def test_form_is_valid(self):
        form = CreateOrderForm(data=self.order_data)
        self.assertTrue(form.is_valid())

    def test_form_with_incorrect_phone_number(self):
        self.order_data['phone'] = '123'
        form = CreateOrderForm(data=self.order_data)
        self.assertFalse(form.is_valid())
