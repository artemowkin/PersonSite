from django.db.models import QuerySet, Model

from generic.services import (
	BaseGetEntryService, BaseModelService, BaseAdminCreateService
)
from .models import Product


class ProductsGetService(BaseGetEntryService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet:
		"""Return all available products"""
		return self.model.objects.filter(available=True)


class ProductCreateService(BaseAdminCreateService):
	"""Service to create a new product entry"""

	model = Product
