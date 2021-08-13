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
from .services.commands import GetAllProductsCommand, CreateProductCommand
from .serializers import ProductSerializer, ProductReviewSerializer


class AllCreateProductsView(BaseAllCreateView):
	"""View to render all products"""

	get_command_class = GetAllProductsCommand
	create_command_class = CreateProductCommand


class ConcreteProductView(BaseConcreteView):
	"""View to render a concrete product"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()
	delete_service = ProductDeleteService()
	serializer_class = ProductSerializer

class ProductImageUploadView(BaseUploadImageView):
	"""View to upload image for product entry"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()


class BaseProductReviewView(APIView):
	"""Base view to render product reviews"""

	permission_classes = [IsAuthenticated]


class AllProductReviewsView(BaseProductReviewView):
	"""View to render all product reviews and create a new"""

	get_product_service = ProductsGetService()
	get_reviews_service_class = ProductReviewsGetService
	create_review_service_class = ProductReviewCreateService
	serializer_class = ProductReviewSerializer

	def get(self, request, pk):
		product = self.get_product_service.get_concrete(pk)
		get_reviews_service = self.get_reviews_service_class(product)
		all_product_reviews = get_reviews_service.get_all()
		overall_rating = count_overall_rating(all_product_reviews)
		serialized_reviews = self.serializer_class(
			all_product_reviews, many=True
		)
		response_data = {
			'overall_rating': overall_rating,
			'reviews': serialized_reviews.data
		}
		return Response(response_data)

	def post(self, request, pk):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			product = self.get_product_service.get_concrete(pk)
			create_review_service = self.create_review_service_class(product)
			review = create_review_service.create(serializer.data, request.user)
			serializer_data = serializer.data
			serializer_data |= {'pk': review.pk}
			return Response(serializer_data, 201)

		return Response(serializer.errors, 400)


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
