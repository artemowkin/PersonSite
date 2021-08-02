from uuid import UUID

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404


class BaseModelService:
	"""Base class for all services using model"""

	model = None

	def __init__(self):
		if not self.model:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have model attribute"
			)


class BaseGetEntryService:
	"""Base service to get entries"""

	def get_concrete(self, pk: UUID) -> Model:
		"""Return a concrete model entry"""
		return get_object_or_404(self.model, pk=pk)

	def get_all(self) -> QuerySet:
		"""Return all model entries"""
		return self.model.objects.all()
