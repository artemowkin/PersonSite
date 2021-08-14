from uuid import UUID

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from generic.services.strategies import CheckIsUserAuthenticatedStrategy
from ..models import Order


User = get_user_model()


class OrderGetService:
	"""Service to get user orders"""

	model = Order

	def __init__(self, user: User):
		self._user = user
		self._check_user_strategy = CheckIsUserAuthenticatedStrategy()
		self._check_user_strategy.check_user(self._user)

	def get_all(self) -> QuerySet[Order]:
		"""Return all user orders"""
		return self.model.objects.filter(customer=self._user)

	def get_concrete(self, pk: UUID) -> Order:
		"""Return a concrete user order"""
		return get_object_or_404(self.model, pk=pk, customer=self._user)


class OrderCreateService:
	"""Service to create a new user order"""

	model = Order

	def __init__(self):
		self._check_user_strategy = CheckIsUserAuthenticatedStrategy()

	def create(self, data: dict, user: User) -> Order:
		"""Create a new user order base on data"""
		self._check_user_strategy.check_user(user)
		order = self.model.objects.create(**data, customer=user)
		return order
