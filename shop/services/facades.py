from uuid import UUID

from generic.services.facades import (
	BaseGetFacade, BaseCreateFacade, BaseUpdateFacade, BaseDeleteFacade
)
from .base import (
	ProductsGetService, ProductReviewsGetService, ProductReviewCreateService,
	ProductReviewUpdateService, ProductReviewDeleteService,
	ProductCreateService, ProductUpdateService, ProductDeleteService,
	count_overall_rating
)
from ..serializers import ProductSerializer, ProductReviewSerializer


class ProductGetFacade(BaseGetFacade):
	"""Facade to get products using services"""

	serializer_class = ProductSerializer

	def __init__(self):
		self.get_service = ProductsGetService()


class ProductCreateFacade(BaseCreateFacade):
	"""Facade to create a new product using services"""

	serializer_class = ProductSerializer

	def __init__(self):
		self.create_service = ProductCreateService()


class ProductUpdateFacade(BaseUpdateFacade):
	"""Facade to update a concrete product using services"""

	serializer_class = ProductSerializer

	def __init__(self):
		self.get_service = ProductsGetService()
		self.update_service = ProductUpdateService()


class ProductDeleteFacade(BaseDeleteFacade):
	"""Facade to delete a concrete product using services"""

	serializer_class = ProductSerializer

	def __init__(self):
		self.get_service = ProductsGetService()
		self.delete_service = ProductDeleteService()


class ProductReviewGetFacade(BaseGetFacade):
	"""Facade to get product reviews using services"""

	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		product_get_service = ProductsGetService()
		product = product_get_service.get_concrete(product_pk)
		self.get_service = ProductReviewsGetService(product)

	def get_all(self) -> tuple[dict, int]:
		"""Return all product reviews with their overall rating"""
		all_reviews = self.get_service.get_all()
		overall_rating = count_overall_rating(all_reviews)
		serialized_reviews = self.serializer_class(all_reviews, many=True).data
		data = {'overall_rating': overall_rating, 'reviews': serialized_reviews}
		return (data, 200)


class ProductReviewCreateFacade(BaseCreateFacade):
	"""Facade to create a new product review using services"""

	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		product_get_service = ProductsGetService()
		product = product_get_service.get_concrete(product_pk)
		self.create_service = ProductReviewCreateService(product)


class ProductReviewUpdateFacade(BaseUpdateFacade):
	"""Facade to update a concrete product review using services"""

	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		product_get_service = ProductsGetService()
		product = product_get_service.get_concrete(product_pk)
		self.get_service = ProductReviewsGetService(product)
		self.update_service = ProductReviewUpdateService()


class ProductReviewDeleteFacade(BaseDeleteFacade):
	"""Facade to delete a concrete product review using services"""

	serializer_class = ProductReviewSerializer

	def __init__(self, product_pk: UUID):
		product_get_service = ProductsGetService()
		product = product_get_service.get_concrete(product_pk)
		self.get_service = ProductReviewsGetService(product)
		self.delete_service = ProductReviewDeleteService()
