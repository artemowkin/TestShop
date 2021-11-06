from .base import FunctionalTest
from products.models import Product, Category


class HomePageFunctionalTests(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(title='test_category')
        for i in range(1, 52):
            Product.objects.create(
                title=f'test_product{i}', price='500.00',
                short_description='test short description',
                description='test description', category=self.category
            )

        self.browser.get(self.live_server_url + '/home/')

    def test_home_page_has_product(self):
        products = self.browser.find_elements('css selector', '.product')
        first_product = products[0]
        first_product_title = first_product.find_element(
            'css selector', '.product_title'
        ).text
        last_product = products[-1]
        last_product_title = last_product.find_element(
            'css selector', '.product_title'
        ).text

        self.assertEqual(len(products), 50)
        self.assertEqual(first_product_title, 'test_product51')
        self.assertEqual(last_product_title, 'test_product2')

