from django.db.models import QuerySet, Model
from django.contrib.auth import get_user_model

from generic.services import (
	BaseGetEntryService, BaseModelService, BaseAdminCreateService,
	check_is_user_superuser
)
from .models import Product


User = get_user_model()


class ProductsGetService(BaseGetEntryService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet:
		"""Return all available products"""
		return self.model.objects.filter(available=True)


class ProductCreateService(BaseAdminCreateService):
	"""Service to create a new product entry"""

	model = Product


class ProductUpdateService:
	"""Service to update the concrete product"""

	def update(self, product: Product, data: dict, user: User) -> Product:
		"""Update the concrete product using data"""
		check_is_user_superuser(user)
		product.title = data['title']
		product.short_description = data['short_description']
		product.description = data['description']
		product.price = data['price']
		product.amount = data['amount']
		product.available = data.get('available') or product.available
		product.save()
		return product
