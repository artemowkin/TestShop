from django.test import LiveServerTestCase
from selenium import webdriver


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

