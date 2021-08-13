from uuid import UUID

from generic.services.commands import BaseGetAllCommand, BaseCreateCommand

from .base import (
	ProductsGetService, ProductCreateService, ProductReviewsGetService,
	count_overall_rating
)
from ..serializers import ProductSerializer, ProductReviewSerializer


class GetAllProductsCommand(BaseGetAllCommand):
	"""Command to get all products"""

	get_service_class = ProductsGetService
	serializer_class = ProductSerializer


class CreateProductCommand(BaseCreateCommand):
	"""Command to create a new product"""

	create_service_class = ProductCreateService
	serializer_class = ProductSerializer


class GetAllProductReviewsCommand:
	"""Base command to get all entries"""

	get_product_service_class = ProductsGetService
	get_review_service_class = ProductReviewsGetService
	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		self._product_pk = product_pk
		self._get_product_service = self.get_product_service_class()

	def _get_all_product_reviews(self):
		"""Get a concrete product and return all reviews on this product"""
		product = self._get_product_service.get_concrete(self._product_pk)
		get_review_service = self._get_review_service_class(product)
		all_product_reviews = get_review_service.get_all()
		return all_product_reviews

	def execute(self) -> tuple[dict, int]:
		"""
		Get all product reviews and return serialized list with these
		reviews, and status code of response
		"""
		all_product_reviews = self._get_all_product_reviews()
		overall_rating = count_overall_rating(all_product_reviews)
		serialized_reviews = self.serializer_class(
			all_product_reviews, many=True
		)
		response_data = {
			'overall_rating': overall_rating,
			'reviews': serialized_reviews.data
		}
		return response_data, 200
