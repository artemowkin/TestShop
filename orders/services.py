from decimal import Decimal

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied
from django.contrib.sessions.backends.db import SessionStore
from django.http import Http404

from .models import Order, Address, Receiver
from cart.services import Cart


User = get_user_model()


class GetOrdersService:
    """Service to get user orders"""

    def __init__(self, user: User) -> None:
        self._user = user
        self._model = Order
        if not self._user.is_authenticated: raise PermissionDenied

    def get_all(self) -> QuerySet:
        """Return all user orders"""
        return self._model.objects.filter(user=self._user)

    def get_concrete(self, pk: int) -> Order:
        """Return a concrete order using pk"""
        return get_object_or_404(self._model, pk=pk, user=self._user)


class CreateOrderService:
    """Service to create a new user order"""

    def __init__(self, user: User, session: SessionStore) -> None:
        self._user = user
        self._cart = Cart(session)
        self._model = Order
        if not self._user.is_authenticated: raise PermissionDenied
        if self._cart.is_empty(): raise Http404

    def create(self, order_data: dict) -> Order:
        """Create a new order using `order_data`"""
        address = self._create_address(order_data)
        receiver = self._create_receiver(order_data)
        cart_products = self._cart.get_products()
        order = self._model.objects.create(
            user=self._user, total_price=Decimal(cart_products['total_sum']),
            address=address, receiver=receiver
        )
        order.products.set(cart_products['products'])
        order.save()
        self._cart.clear()
        return order

    def _create_address(self, order_data: dict) -> Address:
        """Create an address instance"""
        addresses = Address.objects.filter(
            city=order_data['city'], street=order_data['street'],
            house=order_data['house'], apartment=order_data['apartment'],
            postal_code=order_data['postal_code']
        )
        if addresses: return addresses[0]
        address = Address.objects.create(
            city=order_data['city'], street=order_data['street'],
            house=order_data['house'], apartment=order_data['apartment'],
            postal_code=order_data['postal_code']
        )
        return address

    def _create_receiver(self, order_data: dict) -> Receiver:
        """Create a receiver instance"""
        receivers = Receiver.objects.filter(
            first_name=order_data['first_name'],
            last_name=order_data['last_name'], phone=order_data['phone']
        )
        if receivers: return receivers[0]
        receiver = Receiver(
            first_name=order_data['first_name'],
            last_name=order_data['last_name'], phone=order_data['phone']
        )
        receiver.full_clean()
        receiver.save()
        return receiver


def delete_order(user: User, order: Order) -> bool:
    """
    Delete a concrete order and return True if order has been
    deleted else False
    """
    if not user.is_authenticated: raise PermissionDenied
    if user != order.user: raise Http404
    if order.status in ('sent', 'received'): return False
    order.delete()
    return True
