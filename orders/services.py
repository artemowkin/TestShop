from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied

from .models import Order


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
