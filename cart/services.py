from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Sum

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

    def get_products(self) -> dict:
        """Return all products in cart from session"""
        cart_products_pks = self._session['cart']['products']
        products = self._product_model.objects.filter(
            pk__in=cart_products_pks
        )
        total_sum = products.aggregate(
            products_sum=Sum('price')
        )['products_sum']
        return {'products': products, 'total_sum': total_sum}

    def add_product(self, product : Product) -> None:
        """Add the concrete product to cart"""
        session_cart = self._session['cart']
        if not str(product.pk) in session_cart['products']:
            session_cart['products'].append(str(product.pk))
            session_cart['total_sum'] += float(product.price)
            self._session['cart'] = session_cart
            self._session.modified = True

    def clear(self) -> None:
        """Clear products from cart"""
        session_cart = self._session['cart']
        session_cart['products'].clear()
        session_cart['total_sum'] = 0.0
        self._session['cart'] = session_cart
        self._session.modified = True

    def remove_product(self, product : Product) -> None:
        """Remove product from cart"""
        session_cart = self._session['cart']
        if str(product.pk) in session_cart['products']:
            session_cart['products'].remove(str(product.pk))
            session_cart['total_sum'] -= float(product.price)
            self._session['cart'] = session_cart
            self._session.modified = True

