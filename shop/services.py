from uuid import UUID
from typing import TextIO

from django.db.models import QuerySet, Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from generic.services import (
	BaseGetService, BaseModelService, BaseCreateService,
	BaseUpdateService, BaseDeleteService
)
from generic.strategies import (
	CheckIsUserAdminStrategy, CheckIsUserAuthenticatedStrategy
)
from .strategies import CheckIsUserAdminOrAuthorStrategy
from .models import Product, ProductReview


User = get_user_model()


def count_overall_rating(reviews: QuerySet) -> float:
	"""Aggregate average reviews rating"""
	data = reviews.aggregate(overall_rating=Avg('rating'))
	return data['overall_rating']


class ProductsGetService(BaseGetService):
	"""Service to get products entries"""

	model = Product

	def get_all(self) -> QuerySet[Product]:
		"""Get all available products"""
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


class BaseProductReviewService:
	"""Base product reviews service"""

	def __init__(self, product: Product):
		self._product = product


class ProductReviewsGetService(BaseProductReviewService):
	"""Service to get product reviews"""

	model = ProductReview

	def get_all(self) -> QuerySet[ProductReview]:
		"""Return all product reviews"""
		return self._product.reviews.all()

	def get_concrete(self, pk: UUID) -> ProductReview:
		"""Return a concrete product review"""
		return get_object_or_404(self.model, pk=pk, product=self._product)


class ProductReviewCreateService(BaseProductReviewService):
	"""Service to create a new product review"""

	model = ProductReview
	check_user_strategy = CheckIsUserAuthenticatedStrategy()

	def create(self, data: dict, user: User) -> ProductReview:
		"""Create a new product review base on data from user"""
		self.check_user_strategy.check_user(user)
		review = self.model(**data, author=user, product=self._product)
		review.full_clean()
		review.save()
		return review


class ProductReviewUpdateService(BaseUpdateService):
	"""Service to update a concrete product review"""

	check_user_strategy = CheckIsUserAdminOrAuthorStrategy()

	def set_entry_fields(self, entry: Product, data: dict) -> None:
		"""Set product fields using data"""
		entry.text = data['text']
		entry.rating = data['rating']
		entry.full_clean()
