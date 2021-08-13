from uuid import UUID

from generic.services.facades import BaseAPICRUDFacade
from .base import (
	ProductsGetService, ProductReviewsGetService, ProductReviewCreateService,
	ProductReviewUpdateService, ProductReviewDeleteService,
	ProductCreateService, ProductUpdateService, ProductDeleteService,
	count_overall_rating
)
from ..serializers import ProductSerializer, ProductReviewSerializer


class ProductCRUDFacade(BaseAPICRUDFacade):
	"""Facade for product with CRUD functionality using services"""

	serializer_class = ProductSerializer

	def __init__(self):
		self.get_service = ProductsGetService()
		self.create_service = ProductCreateService()
		self.update_service = ProductUpdateService()
		self.delete_service = ProductDeleteService()


class ProductReviewCRUDFacade(BaseAPICRUDFacade):
	"""Facade for product reviews with CRUD functionality using services"""

	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		product_get_service = ProductsGetService()
		product = product_get_service.get_concrete(product_pk)
		self.get_service = ProductReviewsGetService(product)
		self.create_service = ProductReviewCreateService(product)
		self.update_service = ProductReviewUpdateService()
		self.delete_service = ProductReviewDeleteService()

	def get_all(self) -> tuple[dict, int]:
		"""Return all product reviews with their overall rating"""
		all_reviews = self.get_service.get_all()
		overall_rating = count_overall_rating(all_reviews)
		serialized_reviews = self.serializer_class(all_reviews, many=True).data
		data = {'overall_rating': overall_rating, 'reviews': serialized_reviews}
		return (data, 200)
