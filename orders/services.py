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


class CreateAddressService:
    """Service to create a new address for order"""

    def __init__(self, address_data: dict) -> None:
        self._model = Address
        self._address_data = address_data

    def create(self) -> Address:
        """Create an address instance"""
        try:
            address = self._get_or_create_address()
        except MultipleObjectsReturned:
            address = self._handle_multiple_addresses()
            logger.warning("Was founded multiple addresses")

        return address

    def _get_or_create_address(self) -> Address:
        """Create a new address or returns an existing with address_data"""
        address, created = self._model.objects.get_or_create(
            city=self._address_data['city'],
            street=self._address_data['street'],
            house=self._address_data['house'],
            apartment=self._address_data['apartment'],
            postal_code=self._address_data['postal_code']
        )
        logger.debug(f"Created (or getted) address ({address.pk})")
        return address

    def _handle_multiple_addresses(self) -> Address:
        """Handle if addresses are multiple"""
        addresses = self._get_multiple_addresses()
        addresses.delete()
        return self._model.objects.create(
            city=self._address_data['city'],
            street=self._address_data['street'],
            house=self._address_data['house'],
            apartment=self._address_data['apartment'],
            postal_code=self._address_data['postal_code']
        )

    def _get_multiple_addresses(self):
        """Return multiple addresses by address_data"""
        return self._model.objects.filter(
            city=self._address_data['city'],
            street=self._address_data['street'],
            house=self._address_data['house'],
            apartment=self._address_data['apartment'],
            postal_code=self._address_data['postal_code']
        )


class CreateReceiverService:
    """Service to create receiver instance for order"""

    def __init__(self, receiver_data: dict) -> None:
        self._model = Receiver
        self._replace_phone_number(receiver_data)
        self._receiver_data = receiver_data

    def _replace_phone_number(self, order_data: dict) -> None:
        """Replace all symbols in phone number like (, ), +, etc."""
        phone = order_data['phone']
        phone = phone.replace('+7', '8').replace('(', '').replace(
            ')', '').replace('-', '').replace(' ', '')
        order_data['phone'] = phone

    def create(self) -> Receiver:
        """Get or create a receiver instance"""
        receivers = self._get_multiple_receivers()
        if receivers.count() > 1: receivers.delete()
        if receivers:
            logger.debug(f"Getted receiver ({receivers[0].pk})")
            return receivers[0]

        return self._create_receiver_entry()

    def _get_multiple_receivers(self) -> QuerySet:
        """Return queryset with receivers by receiver_data"""
        receivers = self._model.objects.filter(
            first_name=self._receiver_data['first_name'],
            last_name=self._receiver_data['last_name'],
            phone=self._receiver_data['phone']
        )
        return receivers

    def _create_receiver_entry(self) -> Receiver:
        """Create a new receiver entry"""
        receiver = Receiver(
            first_name=self._receiver_data['first_name'],
            last_name=self._receiver_data['last_name'],
            phone=self._receiver_data['phone']
        )
        receiver.full_clean()
        receiver.save()
        logger.debug(f"Created receiver ({receiver.pk})")
        return receiver


class CreateOrderService:
    """Service to create a new user order"""

    def __init__(self, user: User, session: SessionStore) -> None:
        self._user = user
        self._cart = Cart(session)
        self._model = Order
        self._validate_user()
        self._validate_cart()

    def _validate_user(self) -> None:
        """Check is user authenticated"""
        if not self._user.is_authenticated:
            logger.warning(
                'Trying to create an order by not authenticated user'
            )
            raise PermissionDenied

    def _validate_cart(self) -> None:
        """Check is cart not empty"""
        if self._cart.is_empty():
            logger.warning('Trying to create an order with empty cart')
            raise Http404

    def create(self, order_data: dict) -> Order:
        """Create a new order using `order_data`"""
        address = self._create_address(order_data)
        receiver = self._create_receiver(order_data)
        cart_products = self._cart.get_products()
        total_price = Decimal(cart_products['total_sum'])
        products = cart_products['products']
        order = self._create_order_entry(
            total_price, address, receiver, products
        )
        self._cart.clear()
        return order

    def _create_address(self, order_data: dict) -> Order:
        """Create address instance using CreateAddressService"""
        create_address_service = CreateAddressService(order_data)
        return create_address_service.create()

    def _create_receiver(self, order_data: dict) -> Receiver:
        """Create receiver instance using CreateReceiverService"""
        create_receiver_service = CreateReceiverService(order_data)
        return create_receiver_service.create()

    def _create_order_entry(self, total_price: Decimal, address: Address,
            receiver: Receiver, products: QuerySet) -> Order:
        """Create a new order entry"""
        order = self._model.objects.create(
            user=self._user, total_price=total_price,
            address=address, receiver=receiver
        )
        order.products.set(products)
        order.save()
        logger.debug(
            f"Created a new order {order.pk} by user {self._user.email}"
        )
        return order


def delete_order(user: User, order: Order) -> bool:
    """
    Delete a concrete order and return True if order has been
    deleted else False
    """
    _validate_order_user(user, order)
    if not _can_order_be_deleted(order): return False
    order_pk = order.pk
    order.delete()
    logger.debug(f"Deleted order ({order_pk})")
    return True


def _validate_order_user(user: User, order: Order) -> None:
    """Validate is user authenticated and is user an author of order"""
    if not user.is_authenticated: raise PermissionDenied
    if user != order.user: raise Http404


def _can_order_be_deleted(order: Order) -> bool:
    """Check is order status is not 'sent' or 'received'"""
    if order.status in ('sent', 'received'):
        logger.warning(
            f"Trying to delete order {order.pk} with status {order.status}"
        )
        return False

    return True
