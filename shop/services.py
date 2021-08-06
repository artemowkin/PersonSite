from django.db.models import QuerySet

from generic.services import BaseGetEntryService
from .models import Product


class ProductsGetService(BaseGetEntryService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet:
		"""Return all available products"""
		return self.model.objects.filter(available=True)
