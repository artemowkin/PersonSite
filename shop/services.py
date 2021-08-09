from typing import TextIO

from django.db.models import QuerySet, Avg

from generic.services import (
	BaseGetEntryService, BaseModelService, BaseCreateService,
	BaseUpdateService, BaseDeleteService
)
from generic.strategies import CheckIsUserAdminStrategy
from .models import Product, ProductReview


def count_overall_rating(reviews: QuerySet) -> float:
	"""Aggregate average reviews rating"""
	data = reviews.aggregate(overall_rating=Avg('rating'))
	return data['overall_rating']


class ProductsGetService(BaseGetEntryService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet[Product]:
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

	def update_image(self, product: Product, file_obj: TextIO):
		"""Set the image field for product"""
		product.image = file_obj
		product.save()


class ProductDeleteService(BaseDeleteService):
	"""Service to delete a concrete product entry"""

	check_user_strategy = CheckIsUserAdminStrategy()


class ProductReviewsGetService:
	"""Service to get product reviews"""

	def __init__(self, product: Product):
		self._product = product

	def get_all(self) -> QuerySet[ProductReview]:
		"""Return all product reviews"""
		return self._product.reviews.all()
