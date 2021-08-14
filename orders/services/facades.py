from django.contrib.auth import get_user_model

from generic.services.facades import BaseGetFacade, BaseCreateFacade
from .base import OrderGetService, OrderCreateService
from ..serializers import OrderSerializer


User = get_user_model()


class OrderGetFacade(BaseGetFacade):
	"""Facade to get orders using services"""

	serializer_class = OrderSerializer

	def __init__(self, user: User):
		self._user = user
		self.get_service = OrderGetService(self._user)


class OrderCreateFacade(BaseCreateFacade):
	"""Facade to create a new order using services"""

	serializer_class = OrderSerializer

	def __init__(self):
		self.create_service = OrderCreateService()
