from uuid import UUID

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .strategies import CheckUserStrategy


User = get_user_model()


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

	check_user_strategy = CheckUserStrategy()

	def create(self, data: dict, user: User) -> Model:
		"""Create a new entry using data"""
		self.check_user_strategy.check_user(user)
		return self.model.objects.create(**data)


class BaseUpdateService:
	"""Base service to update the concrete entry"""

	check_user_strategy = CheckUserStrategy()

	def set_entry_fields(self, entry: Model, data: dict) -> None:
		"""Set fields for entry using data"""
		raise NotImplementedError

	def update(self, entry: Model, data: dict, user: User) -> Model:
		"""Update the model entry using data"""
		self.check_user_strategy.check_user(user)
		self.set_entry_fields(entry, data)
		entry.save()
		return entry


class BaseDeleteService:
	"""Base service to delete the concrete entry"""

	check_user_strategy = CheckUserStrategy()

	def delete(self, entry: Model, user: User) -> None:
		self.check_user_strategy.check_user(user)
		entry.delete()
