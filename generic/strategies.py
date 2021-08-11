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
