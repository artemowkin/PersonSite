from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from generic.strategies import BaseGetStrategy, BaseModelGetStrategy
from .models import Product, ProductReview


class ProductsGetStrategy(BaseModelGetStrategy):
	"""Strategy to get products with getting all available products"""

	def get_all(self) -> QuerySet[Product]:
		"""Get all available products"""
		return self._model.objects.filter(available=True)


class ProductReviewsGetStrategy(BaseGetStrategy):
	"""Strategy to get product reviews"""

	def __init__(self, model: type, product: Product):
		self._model = model
		self._product = product

	def get_all(self) -> QuerySet[ProductReview]:
		"""Return all product reviews"""
		return self._product.reviews.all()

	def get_concrete(self, pk: UUID) -> ProductReview:
		"""Return a concrete product review"""
		return get_object_or_404(self._model, pk=pk, product=self._product)
