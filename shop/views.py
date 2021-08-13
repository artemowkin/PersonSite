from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import (
	ProductsGetService, ProductCreateService, ProductUpdateService,
	ProductDeleteService, ProductReviewsGetService, ProductReviewCreateService,
	ProductReviewUpdateService, ProductReviewDeleteService,
	count_overall_rating,
)
from .services.commands import (
	GetAllProductsCommand, CreateProductCommand, GetAllProductReviewsCommand,
	CreateProductReviewCommand, GetConcreteProductCommand, UpdateProductCommand,
	DeleteProductCommand
)
from .serializers import ProductSerializer, ProductReviewSerializer


class AllCreateProductsView(BaseAllCreateView):
	"""View to render all products"""

	get_command_class = GetAllProductsCommand
	create_command_class = CreateProductCommand


class ConcreteProductView(BaseConcreteView):
	"""View to render a concrete product"""

	get_command_class = GetConcreteProductCommand
	update_command_class = UpdateProductCommand
	delete_command_class = DeleteProductCommand

class ProductImageUploadView(BaseUploadImageView):
	"""View to upload image for product entry"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()


class BaseProductReviewView(APIView):
	"""Base view to render product reviews"""

	permission_classes = [IsAuthenticated]


class AllProductReviewsView(BaseAllCreateView):
	"""View to render all product reviews and create a new"""

	get_command_class = GetAllProductReviewsCommand
	create_command_class = CreateProductReviewCommand
	permission_classes = [IsAuthenticated]


class ConcreteProductReviewView(BaseProductReviewView):
	"""View to render a concrete product review, update and delete it"""

	get_product_service = ProductsGetService()
	get_reviews_service_class = ProductReviewsGetService
	update_review_service = ProductReviewUpdateService()
	delete_review_service = ProductReviewDeleteService()
	serializer_class = ProductReviewSerializer

	def _get_product_review(self, product_pk, review_pk):
		product = self.get_product_service.get_concrete(product_pk)
		get_reviews_service = self.get_reviews_service_class(product)
		review = get_reviews_service.get_concrete(review_pk)
		return review

	def get(self, request, product_pk, review_pk):
		review = self._get_product_review(product_pk, review_pk)
		serialized_review = self.serializer_class(review)
		return Response(serialized_review.data)

	def put(self, request, product_pk, review_pk):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			review = self._get_product_review(product_pk, review_pk)
			updated_review = self.update_review_service.update(
				review, serializer.data, request.user
			)
			serialized_review = self.serializer_class(updated_review)
			return Response(serialized_review.data)

		return Response(serializer.errors, status=400)

	def delete(self, request, product_pk, review_pk):
		review = self._get_product_review(product_pk, review_pk)
		self.delete_review_service.delete(review, request.user)
		return Response(status=204)
