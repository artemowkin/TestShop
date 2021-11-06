from django.contrib.sessions.backends.db import SessionStore

from products.models import Product
from products.services import GetProductsService


class Cart:
    """Service with shop cart business logic"""
    
    def __init__(self, session: SessionStore) -> None:
        self._session = session
        self._product_model = Product
        self._get_products_service = GetProductsService()
        if not 'cart' in self._session: self._init_cart_session()

    def _init_cart_session(self) -> None:
        """Initialize cart session"""
        self._session['cart'] = {'products': [], 'total_sum': 0.0}

    def add_product(self, product : Product) -> None:
        """Add the concrete product to cart"""
        session_cart = self._session['cart']
        session_cart['products'].append(str(product.pk))
        session_cart['total_sum'] += float(product.price)
        self._session['cart'] = session_cart
        self._session.save()

