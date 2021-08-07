from django.db.models import QuerySet, Model
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from generic.services import (
	BaseGetEntryService, BaseModelService, check_is_user_superuser
)
from .models import Product


User = get_user_model()


class ProductsGetService(BaseGetEntryService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet:
		"""Return all available products"""
		return self.model.objects.filter(available=True)


class ProductCreateService(BaseModelService):
	"""Service to create a new product entry"""

	model = Product

	def create(self, data: dict, user: User) -> Product:
		"""Create a new entry using data"""
		check_is_user_superuser(user)
		return self.model.objects.create(**data)
