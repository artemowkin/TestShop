import logging
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied, MultipleObjectsReturned
from django.contrib.sessions.backends.db import SessionStore
from django.http import Http404

from .models import Order, Address, Receiver
from cart.services import Cart


User = get_user_model()
logger = logging.getLogger('testshop')


class GetOrdersService:
    """Service to get user orders"""

    def __init__(self, user: User) -> None:
        self._user = user
        self._model = Order
        if not self._user.is_authenticated:
            logger.warning('Trying to get orders by not authenticated user')
            raise PermissionDenied

    def get_all(self) -> QuerySet:
        """Return all user orders"""
        logger.debug(f"Getted all orders by user {self._user.email}")
        return self._model.objects.filter(user=self._user)

    def get_concrete(self, pk: int) -> Order:
        """Return a concrete order using pk"""
        logger.debug(f"Getted order {pk} by user {self._user.email}")
        return get_object_or_404(self._model, pk=pk, user=self._user)


class CreateOrderService:
    """Service to create a new user order"""

    def __init__(self, user: User, session: SessionStore) -> None:
        self._user = user
        self._cart = Cart(session)
        self._model = Order
        if not self._user.is_authenticated:
            logger.warning(
                'Trying to create an order by not authenticated user'
            )
            raise PermissionDenied

        if self._cart.is_empty():
            logger.warning('Trying to create an order with empty cart')
            raise Http404

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
        logger.debug(
            f"Created a new order {order.pk} by user {self._user.email}"
        )
        return order

    def _create_address(self, order_data: dict) -> Address:
        """Create an address instance"""
        try:
            address, created = Address.objects.get_or_create(
                city=order_data['city'], street=order_data['street'],
                house=order_data['house'], apartment=order_data['apartment'],
                postal_code=order_data['postal_code']
            )
            logger.debug(f"Created (or getted) address ({address.pk})")
        except MultipleObjectsReturned:
            address = self._handle_multiple_addresses(order_data)
            logger.warning("Was founded multiple addresses")

        return address

    def _handle_multiple_addresses(self) -> Address:
        """Handle if addresses are multiple"""
        addresses = Address.objects.filter(
            city=order_data['city'], street=order_data['street'],
            house=order_data['house'], apartment=order_data['apartment'],
            postal_code=order_data['postal_code']
        )
        addresses.delete()
        return Address.objects.create(
            city=order_data['city'], street=order_data['street'],
            house=order_data['house'], apartment=order_data['apartment'],
            postal_code=order_data['postal_code']
        )

    def _create_receiver(self, order_data: dict) -> Receiver:
        """Create a receiver instance"""
        self._replace_phone_number(order_data)
        receivers = Receiver.objects.filter(
            first_name=order_data['first_name'],
            last_name=order_data['last_name'], phone=order_data['phone']
        )
        if receivers.count() > 1: receivers.delete()
        if receivers:
            logger.debug(f"Getted receiver ({receivers[0].pk})")
            return receivers[0]

        return self._create_receiver_entry(order_data)

    def _create_receiver_entry(self, order_data: dict) -> Receiver:
        """Create a new receiver entry"""
        receiver = Receiver(
            first_name=order_data['first_name'],
            last_name=order_data['last_name'], phone=order_data['phone']
        )
        receiver.full_clean()
        receiver.save()
        logger.debug(f"Created receiver ({receiver.pk})")
        return receiver

    def _replace_phone_number(self, order_data: dict) -> None:
        """Replace all symbols in phone number like (, ), +, etc."""
        phone = order_data['phone']
        phone = phone.replace('+7', '8').replace('(', '').replace(
            ')', '').replace('-', '').replace(' ', '')
        order_data['phone'] = phone


def delete_order(user: User, order: Order) -> bool:
    """
    Delete a concrete order and return True if order has been
    deleted else False
    """
    if not user.is_authenticated: raise PermissionDenied
    if user != order.user: raise Http404
    if order.status in ('sent', 'received'):
        logger.warning(
            f"Trying to delete order {order.pk} with status {order.status}"
        )
        return False

    order_pk = order.pk
    order.delete()
    logger.debug(f"Deleted order ({order_pk})")
    return True
