from uuid import UUID

from django.contrib.auth import get_user_model

from generic.services.commands import (
	BaseGetAllCommand, BaseCreateCommand, BaseGetConcreteCommand,
	BaseUpdateCommand, BaseDeleteCommand
)
from .base import (
	ProductsGetService, ProductCreateService, ProductReviewsGetService,
	ProductReviewCreateService, ProductUpdateService, ProductDeleteService,
	count_overall_rating
)
from ..serializers import ProductSerializer, ProductReviewSerializer


User = get_user_model()


class GetAllProductsCommand(BaseGetAllCommand):
	"""Command to get all products"""

	get_service_class = ProductsGetService
	serializer_class = ProductSerializer


class GetConcreteProductCommand(BaseGetConcreteCommand):
	"""Command to get a concrete product"""

	get_service_class = ProductsGetService
	serializer_class = ProductSerializer


class CreateProductCommand(BaseCreateCommand):
	"""Command to create a new product"""

	create_service_class = ProductCreateService
	serializer_class = ProductSerializer


class UpdateProductCommand(BaseUpdateCommand):
	"""Command to update a concrete product"""

	get_service_class = ProductsGetService
	update_service_class = ProductUpdateService
	serializer_class = ProductSerializer


class DeleteProductCommand(BaseDeleteCommand):
	"""Command to delete a concrete product"""

	get_service_class = ProductsGetService
	delete_service_class = ProductDeleteService
	serializer_class = ProductSerializer


class GetAllProductReviewsCommand:
	"""Command to get all product reviews"""

	get_product_service_class = ProductsGetService
	get_review_service_class = ProductReviewsGetService
	serializer_class = ProductReviewSerializer

	def __init__(self, pk: UUID):
		self._product_pk = pk
		self._get_product_service = self.get_product_service_class()

	def _get_all_product_reviews(self):
		"""Get a concrete product and return all reviews on this product"""
		product = self._get_product_service.get_concrete(self._product_pk)
		get_review_service = self.get_review_service_class(product)
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


class CreateProductReviewCommand:
	"""Command to create a new product review"""

	get_product_service_class = ProductsGetService
	create_review_service_class = ProductReviewCreateService
	serializer_class = ProductReviewSerializer

	def __init__(self, data: dict, user: User, pk: UUID):
		self._data = data
		self._user = user
		self._product_pk = pk
		self._get_product_service = self.get_product_service_class()

	def _create_review(self, serializer: ProductReviewSerializer) -> dict:
		"""Create a new review and return this serialized review"""
		product = self._get_product_service.get_concrete(self._product_pk)
		create_review_service = self.create_review_service_class(product)
		review = create_review_service.create(serializer.data, self._user)
		serialized_review = self.serializer_class(review).data
		return serialized_review

	def execute(self) -> tuple[dict, int]:
		"""
		Get a concrete product and create for this product a new review
		using data and user
		"""
		serializer = self.serializer_class(data=self._data)
		if serializer.is_valid():
			serialized_review = self._create_review(serializer)
			return (serialized_review, 201)

		return (serializer.errors, 400)
