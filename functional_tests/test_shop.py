from .base import FunctionalTest

from products.models import Category, Product


class ShopPageTests(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.first_category = Category.objects.create(title='first category')
        self.second_category = Category.objects.create(title='second category')
        self.first_product = Product.objects.create(
            title='first product', category=self.first_category,
            price='500.00', short_description='some short description',
            description='some description'
        )
        self.second_product = Product.objects.create(
            title='second product', category=self.second_category,
            price='100.00', short_description='some short description',
            description='some description'
        )

    def test_ordering_by_price_to_down(self):
        self.browser.get(self.live_server_url + '/shop?ord_by=price_down')
        products = self.browser.find_elements('css selector', '.product')
        self.assertEqual(len(products), 2)
        first_product_title = products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(first_product_title, self.first_product.title)

    def test_ordering_by_price_to_up(self):
        self.browser.get(self.live_server_url + '/shop?ord_by=price_up')
        products = self.browser.find_elements('css selector', '.product')
        self.assertEqual(len(products), 2)
        first_product_title = products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(first_product_title, self.second_product.title)

    def test_get_all_products(self):
        self.browser.get(self.live_server_url + '/shop/')
        products = self.browser.find_elements('css selector', '.product')
        self.assertEqual(len(products), 2)

    def test_get_products_in_concrete_category(self):
        self.browser.get(
            self.live_server_url + f'/shop?category={self.first_category.pk}'
        )
        products = self.browser.find_elements('css selector', '.product')
        self.assertEqual(len(products), 1)
        product_title = products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(product_title, self.first_product.title)

    def test_get_products_with_concrete_max_price(self):
        self.browser.get(
            self.live_server_url + '/shop?max_price=300'
        )
        products = self.browser.find_elements('css selector', '.product')
        self.assertEqual(len(products), 1)
        product_title = products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(product_title, self.second_product.title)

    def test_get_project_with_search_query(self):
        self.browser.get(
            self.live_server_url + '/shop?query=first'
        )
        products = self.browser.find_elements('css selector', '.product')
        self.assertEqual(len(products), 1)
        product_title = products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(product_title, self.first_product.title)

