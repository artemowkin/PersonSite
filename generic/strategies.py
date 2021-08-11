from uuid import UUID

from django.db.models import Model, QuerySet
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


User = get_user_model()


class CheckUserStrategy:
	"""Strategy with logic to check user authorization"""

	def check_user(self, user: User):
		"""Authorize user"""
		pass


class CheckIsUserAdminStrategy:
	"""Strategy with logic to check is user admin"""

	def check_user(self, user: User):
		"""Check is user admin"""
		if not user.is_superuser:
			raise PermissionDenied


class CheckIsUserAuthenticatedStrategy:
	"""Strategy with logic to check is user authenticated"""

	def check_user(self, user: User):
		"""Check is user authenticated"""
		if not user.is_authenticated:
			raise PermissionDenied


class BaseGetStrategy:
	"""Base strategy with generic logic to get model entries"""

	def get_concrete(self, pk: UUID) -> Model:
		"""
		Return a concrete model entry with pk. Raises Http404
		if not exists
		"""
		return get_object_or_404(self._model, pk=pk)

	def get_all(self) -> QuerySet:
		"""Return all model entries"""
		return self._model.objects.all()


class BaseModelGetStrategy(BaseGetStrategy):
	"""Base get strategy with included model in constructor"""

	def __init__(self, model: type):
		self._model = model


class SimpleGetStrategy(BaseModelGetStrategy):
	"""Strategy with generic logic to get model entries"""

	pass
