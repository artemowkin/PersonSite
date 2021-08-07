from django.db.models import QuerySet, Model
from django.contrib.auth import get_user_model

from generic.services import (
	BaseGetEntryService, BaseModelService, BaseCreateService,
	BaseUpdateService
)
from generic.strategies import CheckIsUserAdminStrategy
from .models import Product


User = get_user_model()


class ProductsGetService(BaseGetEntryService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet:
		"""Return all available products"""
		return self.model.objects.filter(available=True)


class ProductCreateService(BaseCreateService):
	"""Service to create a new product entry"""

	model = Product
	check_user_strategy = CheckIsUserAdminStrategy()


class ProductUpdateService(BaseUpdateService):
	"""Service to update the concrete product"""

	check_user_strategy = CheckIsUserAdminStrategy()

	def set_entry_fields(self, entry: Product, data: dict) -> None:
		"""Set product fields using data"""
		entry.title = data['title']
		entry.short_description = data['short_description']
		entry.description = data['description']
		entry.price = data['price']
		entry.amount = data['amount']
		entry.available = data.get('available') or entry.available
