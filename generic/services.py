from uuid import UUID

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model


def check_is_user_superuser(user: User):
	if not user.is_superuser:
		raise PermissionDenied


class BaseModelService:
	"""Base class for all services using model"""

	model = None

	def __init__(self):
		if not self.model:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have model attribute"
			)


class BaseGetEntryService(BaseModelService):
	"""Base service to get entries"""

	def get_concrete(self, pk: UUID) -> Model:
		"""Return a concrete model entry"""
		return get_object_or_404(self.model, pk=pk)

	def get_all(self) -> QuerySet:
		"""Return all model entries"""
		return self.model.objects.all()


class BaseCreateService(BaseModelService):
	"""Base service to create entries"""

	def check_user(self, user: User):
		"""User authorization"""
		pass

	def create(self, data: dict, user: User) -> Model:
		"""Create a new entry using data"""
		self.check_user(user)
		return self.model.objects.create(**data)


class BaseAdminCreateService(BaseCreateService):
	"""Base service to create entries with checking is user superuser"""

	def check_user(self, user: User):
		"""Check is user supseruser"""
		if not user.is_superuser:
			raise PermissionDenied
