import time

from django.contrib.auth import get_user_model

from .base import FunctionalTest
from products.models import Product, Category
from reviews.models import Review


User = get_user_model()


class ConcreteProductTests(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass',
            email='testuser@gmail.com'
        )
        self.category = Category.objects.create(title='test_category')
        self.product = Product.objects.create(
            title='test_product', price='500.00',
            short_description='test short description',
            description='test description', category=self.category
        )
        self.review = Review.objects.create(
            user=self.user, product=self.product, rating=5, text='some review'
        )
        self.second_product = Product.objects.create(
            title='second product', price='500.00',
            short_description='some short description',
            description='some description', category=self.category
        )
        self.browser.get(self.live_server_url + f'/shop/{self.product.pk}/')

    def test_page_has_product_info(self):
        product_title = self.browser.find_element(
            'css selector', '.product_title'
        ).text
        product_short_description = self.browser.find_element(
            'css selector', '.product_short_description'
        ).text
        product_description = self.browser.find_element(
            'css selector', '.product_description'
        ).text
        product_price = self.browser.find_element(
            'css selector', '.product_price'
        ).text

        self.assertEqual(product_title, self.product.title)
        self.assertEqual(
            product_short_description, self.product.short_description
        )
        self.assertEqual(product_description, self.product.description)
        self.assertEqual(product_price, self.product.price)

    def test_page_has_similar_products(self):
        similar_products = self.browser.find_elements(
            'css selector', '.similar_product'
        )
        self.assertEqual(len(similar_products), 1)
        similar_product = similar_products[0]
        similar_product_title = similar_product.find_element(
            'css selector', '.similar_product_title'
        ).text
        self.assertEqual(similar_product_title, self.second_product.title)

    def test_page_has_reviews(self):
        reviews = self.browser.find_elements(
            'css selector', '.reviews'
        )
        self.assertEqual(len(reviews), 1)
        review_user = reviews[0].find_element(
            'css selector', '.review_user'
        ).text
        review_text = reviews[0].find_element(
            'css selector', '.review_text'
        ).text

        self.assertEqual(review_user, self.user.username)
        self.assertEqual(review_text, self.review.text)

    def test_product_has_add_to_cart_button(self):
        add_to_cart_button = self.browser.find_element(
            'css selector', '.product_add_to_cart'
        )
        self.assertTrue(add_to_cart_button)

    def _login_user(self):
        self.browser.get(self.live_server_url + '/auth/login/')
        login = self.browser.find_element('css selector', '#id_login')
        password = self.browser.find_element('css selector', '#id_password')
        submit = self.browser.find_element('css selector', '.primaryAction')
        login.send_keys('testuser@gmail.com')
        password.send_keys('testpass')
        submit.click()
        time.sleep(1)

    def test_product_add_to_cart(self):
        self._login_user()
        self.browser.get(self.live_server_url + f'/shop/{self.product.pk}/')
        add_to_cart_button = self.browser.find_element(
            'css selector', '.product_add_to_cart'
        )
        add_to_cart_button.click()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/cart/')
        cart_products = self.browser.find_elements(
            'css selector', '.product'
        )
        self.assertEqual(len(cart_products), 1)
        product_title = cart_products[0].find_element(
            'css selector', '.product_title'
        ).text
        self.assertEqual(product_title, self.product.title)

