from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView, BaseCommandView
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
	DeleteProductCommand, GetConcreteProductReviewCommand,
	UpdateProductReviewCommand, DeleteProductReviewCommand
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


class AllProductReviewsView(BaseAllCreateView):
	"""View to render all product reviews and create a new"""

	get_command_class = GetAllProductReviewsCommand
	create_command_class = CreateProductReviewCommand
	permission_classes = [IsAuthenticatedOrReadOnly]


class ConcreteProductReviewView(BaseCommandView):
	"""View to render a concrete product review, update and delete it"""

	get_command_class = GetConcreteProductReviewCommand
	update_command_class = UpdateProductReviewCommand
	delete_command_class = DeleteProductReviewCommand
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request, product_pk, review_pk):
		get_command = self.get_command_class(product_pk, review_pk)
		return self.get_command_response(get_command)

	def put(self, request, product_pk, review_pk):
		update_command = self.update_command_class(
			request.data, request.user, product_pk, review_pk
		)
		return self.get_command_response(update_command)

	def delete(self, request, product_pk, review_pk):
		delete_command = self.delete_command_class(
			request.user, product_pk, review_pk
		)
		return self.get_command_response(delete_command)
