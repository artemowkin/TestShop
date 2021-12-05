from django import template

from products.models import Product
from ..services import Cart


register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product: Product, request) -> bool:
	"""Check is product already in the cart"""
	request_session = request.session
	cart = Cart(request_session)
	return cart.has_product(product)
