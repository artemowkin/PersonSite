from generic.services.facades import BaseAPICRUDFacade
from .base import (
	ProductGetService, ProductReviewGetService, ProductReviewCreateService,
	ProductReviewUpdateService, ProductReviewDeleteService,
	ProductCreateService, ProductUpdateService, ProductDeleteService
)
from ..serializers import ProductSerializer, ProductReviewSerializer


class ProductCRUDFacade(BaseAPICRUDFacade):
	"""Facade for product with CRUD functionality using services"""

	serializer_class = ProductSerializer

	def __init__(self):
		self.get_service = ProductGetService()
		self.create_service = ProductCreateService()
		self.update_service = ProductUpdateService()
		self.delete_service = ProductDeleteService()


class ProductReviewCRUDFacade(BaseAPICRUDFacade):
	"""Facade for product reviews with CRUD functionality using services"""

	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		product_get_service = ProductGetService()
		product = product_get_service.get_concrete(product_pk)
		self.get_service = ProductReviewGetService(product)
		self.create_service = ProductReviewCreateService(product)
		self.update_service = ProductReviewUpdateService()
		self.delete_service = ProductReviewDeleteService()
